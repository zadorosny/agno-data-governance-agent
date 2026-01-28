import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import json
import re
import pandas as pd
from agno.models.message import Message

from agents.pii_detector import PIIDetectorAgent
from agents.data_classifier import DataClassifierAgent

def extract_json(raw_text: str):
    """
    Extrai JSON de respostas LLM de forma robusta.
    Prioriza OBJETO antes de LISTA.
    """
    
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
        return parsed
    except Exception:
        pass

    obj_match = re.search(r"\{[\s\S]*\}", cleaned)
    if obj_match:
        try:
            return json.loads(obj_match.group())
        except Exception:
            pass

    list_match = re.search(r"\[[\s\S]*\]", cleaned)
    if list_match:
        try:
            return json.loads(list_match.group())
        except Exception:
            pass

    raise ValueError("Não foi possível extrair JSON válido da resposta do LLM")

def normalize_pii_output(raw_text: str, valid_columns: list[str]):
    data = extract_json(raw_text)
    return [
        item for item in data
        if item.get("column") in valid_columns
    ]

def run_credit_governance_pipeline(csv_path: str):
    
    df = pd.read_csv(csv_path)
    print(f"Dataset carregado com {len(df)} registros")

    pii_payload = {
        "columns": list(df.columns),
        "sample_rows": df.head(3).to_dict(orient="records")
    }

    pii_message = Message(
        role="user",
        content=json.dumps(pii_payload, ensure_ascii=False)
    )

    pii_result = PIIDetectorAgent.run(pii_message)

    print(pii_result.content)

    pii_normalized = normalize_pii_output(
        pii_result.content,
        valid_columns=list(df.columns)
    )

    print(json.dumps(pii_normalized, indent=2, ensure_ascii=False))

    classifier_message = Message(
        role="user",
        content=json.dumps(pii_normalized, ensure_ascii=False)
    )

    classifier_result = DataClassifierAgent.run(classifier_message)
    
    print(classifier_result.content)

    governance_decision = extract_json(classifier_result.content)
   
    print(json.dumps(governance_decision, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run_credit_governance_pipeline("data/sample_credit_portfolio.csv")
