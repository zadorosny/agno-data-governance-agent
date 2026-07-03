"""Testes unitários para utils.json_parser (não requerem API)."""

import pytest

from utils.json_parser import extract_json, extract_json_dict, normalize_pii_output


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

    def test_parse_nested_object_with_surrounding_text(self):
        raw = 'Aqui está:\n{"policies": {"retention": {"duration": 5}}}\nFim.'
        assert extract_json(raw) == {"policies": {"retention": {"duration": 5}}}

    def test_parse_object_with_braces_inside_strings(self):
        raw = 'Resultado: {"justification": "risco {alto} conforme LGPD"}'
        assert extract_json(raw) == {"justification": "risco {alto} conforme LGPD"}

    def test_parse_list_with_surrounding_text(self):
        raw = 'Colunas sensíveis:\n[{"column": "cpf"}, {"column": "score"}]\nFim.'
        assert extract_json(raw) == [{"column": "cpf"}, {"column": "score"}]

    def test_prefers_payload_over_list_reference_in_text(self):
        raw = 'Conforme [1], o resultado é {"key": "value"}.'
        assert extract_json(raw) == {"key": "value"}

    def test_raises_on_invalid(self):
        with pytest.raises(ValueError, match="Não foi possível extrair JSON"):
            extract_json("texto sem json nenhum")

    def test_raises_on_none_content(self):
        # RunOutput.content do agno é Optional[Any]
        with pytest.raises(TypeError, match="sem conteúdo textual"):
            extract_json(None)


class TestExtractJsonDict:
    def test_returns_dict(self):
        assert extract_json_dict('{"key": "value"}') == {"key": "value"}

    def test_raises_on_list(self):
        with pytest.raises(TypeError, match="Esperado objeto JSON"):
            extract_json_dict('[{"a": 1}]')


class TestNormalizePiiOutput:
    def test_filters_invalid_columns(self):
        raw = '[{"column": "cpf", "data_type": "PII"}, {"column": "fake_col", "data_type": "PII"}]'
        result = normalize_pii_output(raw, valid_columns=["cpf", "renda"])
        assert len(result) == 1
        assert result[0]["column"] == "cpf"

    def test_filters_non_dict_items(self):
        raw = '["cpf", {"column": "cpf", "data_type": "PII"}, 42]'
        result = normalize_pii_output(raw, valid_columns=["cpf"])
        assert result == [{"column": "cpf", "data_type": "PII"}]

    def test_raises_on_non_list(self):
        with pytest.raises(TypeError, match="Esperado lista"):
            normalize_pii_output('{"key": "value"}', valid_columns=["cpf"])
