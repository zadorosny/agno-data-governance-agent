"""Utilitários para extração e normalização de JSON de respostas LLM."""

from __future__ import annotations

import json

from config import get_logger

logger = get_logger(__name__)


def extract_json(raw_text: str) -> dict | list:
    """Extrai JSON de respostas LLM de forma robusta.

    Tenta parse direto do texto limpo; se falhar, varre o texto com
    ``json.JSONDecoder.raw_decode`` (que lida com aninhamento e chaves dentro
    de strings, ao contrário de regex) e retorna o candidato válido mais longo
    — o payload é sempre o maior trecho JSON, enquanto artefatos do texto ao
    redor (ex.: referências "[1]") são curtos.

    Raises:
        ValueError: se nenhuma estratégia produzir JSON válido.
    """
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    best: dict | list | None = None
    best_length = 0
    for i, char in enumerate(cleaned):
        if char in "{[":
            try:
                value, end = decoder.raw_decode(cleaned, i)
            except json.JSONDecodeError:
                continue
            if end - i > best_length:
                best, best_length = value, end - i
    if best is not None:
        return best

    raise ValueError(
        f"Não foi possível extrair JSON válido da resposta do LLM. "
        f"Primeiros 200 chars: {raw_text[:200]!r}"
    )


def extract_json_dict(raw_text: str) -> dict:
    """Extrai JSON da resposta do LLM garantindo que o resultado seja um objeto (dict).

    Raises:
        TypeError: se o JSON extraído não for um objeto.
    """
    data = extract_json(raw_text)
    if not isinstance(data, dict):
        raise TypeError(f"Esperado objeto JSON do LLM, recebeu {type(data).__name__}")
    return data


def normalize_pii_output(raw_text: str, valid_columns: list[str]) -> list[dict]:
    """Extrai e filtra saída do PII Detector, mantendo apenas colunas existentes."""
    data = extract_json(raw_text)

    if not isinstance(data, list):
        raise TypeError(f"Esperado lista do PII Detector, recebeu {type(data).__name__}")

    filtered = [item for item in data if isinstance(item, dict) and item.get("column") in valid_columns]

    removed = len(data) - len(filtered)
    if removed:
        logger.warning("PII Detector: %d itens removidos (colunas inexistentes)", removed)

    return filtered
