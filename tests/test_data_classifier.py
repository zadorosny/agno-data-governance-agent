"""Teste de integração: Data Classifier Agent."""

import json

import pytest
from agno.models.message import Message

from agents.data_classifier import DataClassifierAgent
from utils.json_parser import extract_json


@pytest.mark.integration
def test_data_classifier_returns_valid_structure(sample_pii_result: list[dict]):
    message = Message(role="user", content=json.dumps(sample_pii_result, ensure_ascii=False))
    result = DataClassifierAgent.run(message)

    classification = extract_json(result.content)

    assert isinstance(classification, dict)
    assert "dataset_risk" in classification
    assert "lgpd_legal_basis" in classification
