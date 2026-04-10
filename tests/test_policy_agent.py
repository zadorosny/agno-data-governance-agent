"""Teste de integração: Policy Agent."""

import json

import pytest
from agno.models.message import Message

from agents.policy_agent import PolicyAgent
from utils.json_parser import extract_json


@pytest.mark.integration
def test_policy_agent_returns_valid_structure(sample_policy_input: dict):
    message = Message(role="user", content=json.dumps(sample_policy_input, ensure_ascii=False))
    result = PolicyAgent.run(message)

    policies = extract_json(result.content)

    assert isinstance(policies, dict)
    assert "retention_policy" in policies
    assert "access_policy" in policies
