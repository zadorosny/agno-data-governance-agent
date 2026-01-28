import json
import os
from agno.models.message import Message
from agents.compliance_reporter import ComplianceReporterAgent


input_payload = {
    "dataset_name": "credit_portfolio",
    "dataset_risk": "high_risk",
    "lgpd_legal_basis": "obrigação legal/regulatória",
    "policies": {
        "retention_policy": {
            "duration": 5,
            "description": "Retenção mínima exigida por regulamentação financeira."
        },
        "masking_policy": {
            "cpf": "hashing SHA-256",
            "identificadores": "mascaramento parcial"
        },
        "access_policy": [
            "Equipe de Crédito",
            "Equipe de Risco",
            "Compliance"
        ]
    },
    "lineage_summary": {
        "source": "Sistemas internos de crédito",
        "consumers": [
            "Motor de crédito",
            "Monitoramento de risco",
            "Relatórios regulatórios"
        ],
        "risk_points": [
            "Exposição de CPF",
            "Uso indevido de score",
            "Retenção excessiva"
        ]
    }
}

message = Message(
    role="user",
    content=json.dumps(input_payload, ensure_ascii=False)
)

result = ComplianceReporterAgent.run(message)

print(result.content)

os.makedirs("reports", exist_ok=True)

with open("reports/compliance_report.md", "w", encoding="utf-8") as f:
    f.write(result.content)
