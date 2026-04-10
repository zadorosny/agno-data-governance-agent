"""Utilitários para extração e normalização de JSON de respostas LLM."""

from __future__ import annotations

import json
import re

from config import get_logger

logger = get_logger(__name__)


def extract_json(raw_text: str) -> dict | list:
    """Extrai JSON de respostas LLM de forma robusta.

    Tenta, em ordem:
      1. Parse direto do texto limpo
      2. Regex para objeto JSON ``{...}``
      3. Regex para lista JSON ``[...]``

    Raises:
        ValueError: se nenhuma estratégia produzir JSON válido.
    """
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    obj_match = re.search(r"\{[\s\S]*?\}(?![\s\S]*\{)", cleaned)
    if not obj_match:
        obj_match = re.search(r"\{[\s\S]+\}", cleaned)
    if obj_match:
        try:
            return json.loads(obj_match.group())
        except json.JSONDecodeError:
            logger.warning("Regex encontrou candidato a objeto JSON, mas parse falhou")

    list_match = re.search(r"\[[\s\S]+\]", cleaned)
    if list_match:
        try:
            return json.loads(list_match.group())
        except json.JSONDecodeError:
            logger.warning("Regex encontrou candidato a lista JSON, mas parse falhou")

    raise ValueError(
        f"Não foi possível extrair JSON válido da resposta do LLM. "
        f"Primeiros 200 chars: {raw_text[:200]!r}"
    )


def normalize_pii_output(raw_text: str, valid_columns: list[str]) -> list[dict]:
    """Extrai e filtra saída do PII Detector, mantendo apenas colunas existentes."""
    data = extract_json(raw_text)

    if not isinstance(data, list):
        raise TypeError(f"Esperado lista do PII Detector, recebeu {type(data).__name__}")

    filtered = [item for item in data if item.get("column") in valid_columns]

    removed = len(data) - len(filtered)
    if removed:
        logger.warning("PII Detector: %d itens removidos (colunas inexistentes)", removed)

    return filtered
