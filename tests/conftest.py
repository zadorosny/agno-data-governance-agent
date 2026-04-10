"""Fixtures compartilhados para os testes de integração dos agentes."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from config import DATA_DIR


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sample_credit_portfolio.csv")


@pytest.fixture
def pii_payload(sample_df: pd.DataFrame) -> dict:
    return {
        "columns": list(sample_df.columns),
        "sample_rows": sample_df.head(3).to_dict(orient="records"),
    }


@pytest.fixture
def sample_pii_result() -> list[dict]:
    return [
        {"column": "cpf", "data_type": "PII", "risk_level": "high"},
        {"column": "monthly_income", "data_type": "Financial", "risk_level": "medium"},
        {"column": "credit_limit", "data_type": "Financial", "risk_level": "medium"},
        {"column": "credit_score", "data_type": "Financial", "risk_level": "high"},
        {"column": "default_flag", "data_type": "Behavioral", "risk_level": "medium"},
        {"column": "customer_id", "data_type": "PII", "risk_level": "high"},
    ]


@pytest.fixture
def sample_classification() -> dict:
    return {
        "dataset_risk": "high_risk",
        "lgpd_legal_basis": "obrigação legal/regulatória",
        "justification": "Dataset contém PII e dados financeiros sensíveis.",
        "allowed_use_cases": ["políticas de crédito"],
    }


@pytest.fixture
def sample_lineage_input() -> dict:
    return {
        "dataset_name": "credit_portfolio",
        "domain": "crédito",
        "description": "Dataset utilizado para políticas de crédito e monitoramento de risco",
    }


@pytest.fixture
def sample_policy_input() -> dict:
    return {
        "dataset_risk": "high_risk",
        "lgpd_legal_basis": "obrigação legal/regulatória",
        "data_types": ["PII", "Financial", "Behavioral"],
    }


@pytest.fixture
def sample_report_input() -> dict:
    return {
        "dataset_name": "credit_portfolio",
        "dataset_risk": "high_risk",
        "lgpd_legal_basis": "obrigação legal/regulatória",
        "policies": {
            "retention_policy": {"duration": 5, "description": "Retenção mínima exigida por regulamentação financeira."},
            "masking_policy": {"cpf": "hashing SHA-256", "identificadores": "mascaramento parcial"},
            "access_policy": ["Equipe de Crédito", "Equipe de Risco", "Compliance"],
        },
        "lineage_summary": {
            "source": "Sistemas internos de crédito",
            "consumers": ["Motor de crédito", "Monitoramento de risco", "Relatórios regulatórios"],
            "risk_points": ["Exposição de CPF", "Uso indevido de score", "Retenção excessiva"],
        },
    }
