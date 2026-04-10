"""Teste de integração: PII Detector Agent."""

import json

import pytest
from agno.models.message import Message

from agents.pii_detector import PIIDetectorAgent
from utils.json_parser import normalize_pii_output


@pytest.mark.integration
def test_pii_detector_returns_valid_json(pii_payload: dict, sample_df):
    message = Message(role="user", content=json.dumps(pii_payload, ensure_ascii=False))
    result = PIIDetectorAgent.run(message)

    normalized = normalize_pii_output(result.content, valid_columns=list(sample_df.columns))

    assert isinstance(normalized, list)
    assert len(normalized) > 0
    for item in normalized:
        assert "column" in item
        assert "data_type" in item
        assert "risk_level" in item
