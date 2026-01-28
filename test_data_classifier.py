import json
import re
from agno.models.message import Message
from agents.data_classifier import DataClassifierAgent

pii_result = [
    {"column": "cpf", "data_type": "PII", "risk_level": "high"},
    {"column": "monthly_income", "data_type": "Financial", "risk_level": "medium"},
    {"column": "credit_limit", "data_type": "Financial", "risk_level": "medium"},
    {"column": "credit_score", "data_type": "Financial", "risk_level": "high"},
    {"column": "default_flag", "data_type": "Behavioral", "risk_level": "medium"},
    {"column": "customer_id", "data_type": "PII", "risk_level": "high"}
]

message = Message(
    role="user",
    content=json.dumps(pii_result, ensure_ascii=False)
)

result = DataClassifierAgent.run(message)

raw_output = result.content
print(raw_output)


def normalize_classifier_output(raw_text: str):
    try:
        return json.loads(raw_text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", raw_text)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    raise ValueError("Não foi possível extrair JSON válido do classificador")

clean_result = normalize_classifier_output(raw_output)

print(json.dumps(clean_result, indent=2, ensure_ascii=False))
