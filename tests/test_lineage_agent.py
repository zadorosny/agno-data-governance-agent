"""Teste de integração: Lineage Agent."""

import json

import pytest
from agno.models.message import Message

from agents.lineage_agent import LineageAgent
from utils.json_parser import extract_json


@pytest.mark.integration
def test_lineage_agent_returns_valid_structure(sample_lineage_input: dict):
    message = Message(role="user", content=json.dumps(sample_lineage_input, ensure_ascii=False))
    result = LineageAgent.run(message)

    lineage = extract_json(result.content)

    assert isinstance(lineage, dict)
    assert "source" in lineage
    assert "consumers" in lineage
