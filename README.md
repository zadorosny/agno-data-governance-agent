# agno-data-governance-agent

Sistema multiagente baseado em IA para governança de dados sensíveis, com foco em datasets de crédito e portfólio financeiro, aplicando princípios da LGPD, risco regulatório e boas práticas de compliance.

O projeto simula como fintechs, bancos e instituições financeiras podem utilizar agentes de IA para apoiar decisões de governança de dados, sem substituir controles humanos, cobrindo desde a identificação de PII até a geração de relatórios executivos de compliance.

Feito utilizando o modelo de LLM llama-3.1-8b-instant, por meio do Groq Cloud (https://console.groq.com/home)

## Objetivo do Projeto

Demonstrar, de forma prática e aplicada, como a IA pode apoiar processos de governança de dados em ambientes regulados, incluindo:

- Identificação de dados pessoais e financeiros sensíveis (PII)
- Classificação de risco regulatório conforme LGPD
- Definição de políticas de governança de dados
- Mapeamento de linhagem de dados (data lineage)
- Geração de relatórios executivos para áreas de risco, compliance e auditoria

O foco do projeto são dados de crédito, comuns em fintechs, bancos e instituições financeiras.

## Visão Geral da Arquitetura

O sistema é composto por agentes especializados, cada um com uma responsabilidade clara, seguindo princípios de separação de responsabilidades, validação defensiva das respostas do LLM e uso da IA como suporte à decisão.

Fluxo geral do sistema:

```
Dataset de Crédito
→ PII Detector Agent
→ Data Classifier Agent (LGPD / Risco)
→ Lineage Agent (Linhagem de Dados)
→ Policy Agent (Políticas de Governança)
→ Compliance Reporter Agent (Relatório Executivo)
```

Para detalhes, consulte [docs/architecture.md](docs/architecture.md).

## Agentes Implementados

| Agente | Responsabilidade |
|---|---|
| **PII Detector** | Identifica dados sensíveis por coluna (CPF, renda, score, inadimplência) |
| **Data Classifier** | Classifica risco regulatório, base legal LGPD e casos de uso permitidos |
| **Lineage Agent** | Mapeia origem, transformações, consumidores e riscos dos dados |
| **Policy Agent** | Define políticas de retenção, mascaramento e controle de acesso |
| **Compliance Reporter** | Gera relatório executivo em Markdown para gestores e auditoria |

## Como Executar

### Pré-requisitos

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/zadorosny/agno-data-governance-agent.git
cd agno-data-governance-agent

# Copiar e configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves de API

# Instalar dependências (com uv)
uv sync

# Ou com pip
pip install -r requirements.txt
```

### Executar o pipeline completo

```bash
python pipelines/credit_governance_pipeline.py
```

### Executar testes

```bash
# Testes unitários (não requerem API)
pytest tests/test_json_parser.py -v

# Testes de integração (requerem GROQ_API_KEY)
pytest tests/ -m integration -v
```

## Decisões Arquiteturais

- As respostas dos agentes não assumem saída perfeita do LLM. O parsing e a validação ocorrem na camada de consumo.
- A IA atua como suporte à governança e compliance, não como decisora final.
- Configuração centralizada em `config.py` para evitar valores hardcoded espalhados.

## Contexto de Uso

Projeto relevante para fintechs, bancos, instituições financeiras e times de dados, risco e compliance, especialmente em ambientes regulados por LGPD, crédito e fraude.

## Possíveis Extensões

- Integração com catálogos de dados
- Validação automática de políticas
- Exportação de relatórios para PDF
- Integração com ferramentas de BI ou Data Governance

## Licença

Projeto desenvolvido para fins educacionais e de portfólio. Licença MIT.
