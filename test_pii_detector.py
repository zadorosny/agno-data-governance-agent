import json
import pandas as pd
from agno.models.message import Message

from agents.pii_detector import PIIDetectorAgent


df = pd.read_csv("data/sample_credit_portfolio.csv")

payload = {
    "columns": list(df.columns),
    "sample_rows": df.head(3).to_dict(orient="records")
}


message = Message(
    role="user",
    content=json.dumps(payload, ensure_ascii=False)
)

result = PIIDetectorAgent.run(message)

raw_output = result.content


def normalize_pii_output(raw_text: str, valid_columns: list[str]):
    """
    Normaliza a saída do LLM:
    - garante JSON válido
    - remove colunas inexistentes
    - evita confiar cegamente no modelo
    """
    try:
        data = json.loads(
            raw_text.replace("```json", "").replace("```", "").strip()
        )
    except json.JSONDecodeError:
        raise ValueError("Resposta do modelo não é um JSON válido")

    normalized = [
        item for item in data
        if item.get("column") in valid_columns
    ]

    return normalized


clean_result = normalize_pii_output(
    raw_output,
    valid_columns=list(df.columns)
)

print(json.dumps(clean_result, indent=2, ensure_ascii=False))
