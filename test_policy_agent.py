import json
import re
from agno.models.message import Message
from agents.policy_agent import PolicyAgent

def extract_json(raw_text: str):
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        return json.loads(match.group())

    raise ValueError("Não foi possível extrair JSON válido do PolicyAgent")

input_payload = {
    "dataset_risk": "high_risk",
    "lgpd_legal_basis": "obrigação legal/regulatória",
    "data_types": ["PII", "Financial", "Behavioral"]
}

message = Message(
    role="user",
    content=json.dumps(input_payload, ensure_ascii=False)
)

result = PolicyAgent.run(message)

print(result.content)

policy = extract_json(result.content)

print(json.dumps(policy, indent=2, ensure_ascii=False))
