"""Teste de integração: Compliance Reporter Agent."""

import json

import pytest
from agno.models.message import Message

from agents.compliance_reporter import ComplianceReporterAgent


@pytest.mark.integration
def test_compliance_reporter_returns_markdown(sample_report_input: dict):
    message = Message(role="user", content=json.dumps(sample_report_input, ensure_ascii=False))
    result = ComplianceReporterAgent.run(message)

    assert isinstance(result.content, str)
    assert len(result.content) > 100
    assert "#" in result.content  # contém headers Markdown
