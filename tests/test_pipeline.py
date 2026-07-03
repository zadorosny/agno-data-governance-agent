"""Teste unitário do pipeline com agentes simulados (não requer API)."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import pipelines.credit_governance_pipeline as pipeline
from config import DATA_DIR


def _stub(content: str):
    return lambda message: SimpleNamespace(content=content)


@pytest.fixture
def stubbed_agents(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Substitui o .run de cada agente por respostas canônicas e isola REPORTS_DIR."""
    pii = [
        {"column": "cpf", "data_type": "PII", "risk_level": "high"},
        {"column": "credit_score", "data_type": "Financial", "risk_level": "high"},
        {"column": "coluna_inexistente", "data_type": "PII", "risk_level": "high"},
    ]
    classification = {
        "dataset_risk": "high_risk",
        "lgpd_legal_basis": "obrigação legal/regulatória",
        "justification": "Contém PII e dados financeiros.",
        "allowed_use_cases": ["políticas de crédito"],
    }
    lineage = {"source": "core bancário", "transformations": [], "consumers": [], "risk_points": []}
    policies = {"retention_policy": "5 anos", "masking_policy": "hash de CPF", "access_policy": ["Crédito"]}

    monkeypatch.setattr(pipeline.PIIDetectorAgent, "run", _stub(json.dumps(pii)))
    monkeypatch.setattr(pipeline.DataClassifierAgent, "run", _stub(json.dumps(classification)))
    monkeypatch.setattr(pipeline.LineageAgent, "run", _stub(json.dumps(lineage)))
    monkeypatch.setattr(pipeline.PolicyAgent, "run", _stub(json.dumps(policies)))
    monkeypatch.setattr(pipeline.ComplianceReporterAgent, "run", _stub("# Relatório de Compliance\n\nOK."))
    monkeypatch.setattr(pipeline, "REPORTS_DIR", tmp_path)
    return tmp_path


def test_pipeline_end_to_end_with_stubs(stubbed_agents):
    result = pipeline.run_credit_governance_pipeline(DATA_DIR / "sample_credit_portfolio.csv")

    # Colunas inexistentes no dataset são descartadas pela normalização
    assert [item["column"] for item in result["pii"]] == ["cpf", "credit_score"]
    assert result["classification"]["dataset_risk"] == "high_risk"
    assert result["lineage"]["source"] == "core bancário"
    assert result["policies"]["retention_policy"] == "5 anos"

    report = stubbed_agents / "compliance_report.md"
    assert result["report_path"] == str(report)
    assert report.read_text(encoding="utf-8").startswith("# Relatório de Compliance")


def test_pipeline_raises_on_missing_dataset(stubbed_agents):
    with pytest.raises(FileNotFoundError):
        pipeline.run_credit_governance_pipeline("nao_existe.csv")
