"""Testes unitários para utils.json_parser (não requerem API)."""

import pytest

from utils.json_parser import extract_json, normalize_pii_output


class TestExtractJson:
    def test_parse_clean_object(self):
        result = extract_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_clean_list(self):
        result = extract_json('[{"a": 1}]')
        assert result == [{"a": 1}]

    def test_parse_with_markdown_fences(self):
        raw = '```json\n{"key": "value"}\n```'
        assert extract_json(raw) == {"key": "value"}

    def test_parse_with_surrounding_text(self):
        raw = 'Aqui está o resultado:\n{"key": "value"}\nFim.'
        assert extract_json(raw) == {"key": "value"}

    def test_raises_on_invalid(self):
        with pytest.raises(ValueError, match="Não foi possível extrair JSON"):
            extract_json("texto sem json nenhum")


class TestNormalizePiiOutput:
    def test_filters_invalid_columns(self):
        raw = '[{"column": "cpf", "data_type": "PII"}, {"column": "fake_col", "data_type": "PII"}]'
        result = normalize_pii_output(raw, valid_columns=["cpf", "renda"])
        assert len(result) == 1
        assert result[0]["column"] == "cpf"

    def test_raises_on_non_list(self):
        with pytest.raises(TypeError, match="Esperado lista"):
            normalize_pii_output('{"key": "value"}', valid_columns=["cpf"])
