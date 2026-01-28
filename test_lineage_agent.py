import json
import re
from agno.models.message import Message
from agents.lineage_agent import LineageAgent


def extract_json(raw_text: str):
    """
    Extrai JSON (objeto) de respostas LLM de forma robusta.
    """
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        return json.loads(match.group())

    raise ValueError("Não foi possível extrair JSON válido do LineageAgent")


input_payload = {
    "dataset_name": "credit_portfolio",
    "domain": "crédito",
    "description": "Dataset utilizado para políticas de crédito e monitoramento de risco"
}

message = Message(
    role="user",
    content=json.dumps(input_payload, ensure_ascii=False)
)

result = LineageAgent.run(message)

print(result.content)

lineage = extract_json(result.content)

print(json.dumps(lineage, indent=2, ensure_ascii=False))
