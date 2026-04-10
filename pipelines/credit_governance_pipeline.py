"""Pipeline completo de governança de dados de crédito."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from agno.models.message import Message

from agents.compliance_reporter import ComplianceReporterAgent
from agents.data_classifier import DataClassifierAgent
from agents.lineage_agent import LineageAgent
from agents.pii_detector import PIIDetectorAgent
from agents.policy_agent import PolicyAgent
from config import DATA_DIR, REPORTS_DIR, get_logger
from utils.json_parser import extract_json, normalize_pii_output

logger = get_logger(__name__)


def run_credit_governance_pipeline(csv_path: str | Path) -> dict:
    """Executa o pipeline sequencial de governança sobre um dataset de crédito.

    Returns:
        Dicionário com os resultados de cada etapa do pipeline.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    logger.info("Dataset carregado: %s (%d registros, %d colunas)", csv_path.name, len(df), len(df.columns))

    # --- 1. Detecção de PII ---
    pii_payload = {
        "columns": list(df.columns),
        "sample_rows": df.head(3).to_dict(orient="records"),
    }
    pii_response = PIIDetectorAgent.run(
        Message(role="user", content=json.dumps(pii_payload, ensure_ascii=False))
    )
    pii_normalized = normalize_pii_output(pii_response.content, valid_columns=list(df.columns))
    logger.info("PII detectado: %d colunas sensíveis", len(pii_normalized))

    # --- 2. Classificação de risco ---
    classifier_response = DataClassifierAgent.run(
        Message(role="user", content=json.dumps(pii_normalized, ensure_ascii=False))
    )
    classification = extract_json(classifier_response.content)
    logger.info("Classificação: %s", classification.get("dataset_risk", "N/A"))

    # --- 3. Linhagem de dados ---
    lineage_payload = {
        "dataset_name": csv_path.stem,
        "domain": "crédito",
        "description": "Dataset utilizado para políticas de crédito e monitoramento de risco",
    }
    lineage_response = LineageAgent.run(
        Message(role="user", content=json.dumps(lineage_payload, ensure_ascii=False))
    )
    lineage = extract_json(lineage_response.content)
    logger.info("Linhagem mapeada: origem=%s", lineage.get("source", "N/A"))

    # --- 4. Políticas de governança ---
    policy_payload = {
        "dataset_risk": classification.get("dataset_risk"),
        "lgpd_legal_basis": classification.get("lgpd_legal_basis"),
        "data_types": list({item.get("data_type") for item in pii_normalized}),
    }
    policy_response = PolicyAgent.run(
        Message(role="user", content=json.dumps(policy_payload, ensure_ascii=False))
    )
    policies = extract_json(policy_response.content)
    logger.info("Políticas definidas")

    # --- 5. Relatório de compliance ---
    report_payload = {
        "dataset_name": csv_path.stem,
        "dataset_risk": classification.get("dataset_risk"),
        "lgpd_legal_basis": classification.get("lgpd_legal_basis"),
        "policies": policies,
        "lineage_summary": lineage,
    }
    report_response = ComplianceReporterAgent.run(
        Message(role="user", content=json.dumps(report_payload, ensure_ascii=False))
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "compliance_report.md"
    report_path.write_text(report_response.content, encoding="utf-8")
    logger.info("Relatório salvo em %s", report_path)

    return {
        "pii": pii_normalized,
        "classification": classification,
        "lineage": lineage,
        "policies": policies,
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    result = run_credit_governance_pipeline(DATA_DIR / "sample_credit_portfolio.csv")
    print(json.dumps(result, indent=2, ensure_ascii=False))
