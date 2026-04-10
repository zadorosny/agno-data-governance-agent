# agno-data-governance-agent

Sistema multiagente baseado em IA para governança de dados sensíveis, com foco em datasets de crédito e portfólio financeiro, aplicando princípios da LGPD, risco regulatório e boas práticas de compliance.

O projeto simula como fintechs, bancos e instituições financeiras podem utilizar agentes de IA para apoiar decisões de governança de dados, sem substituir controles humanos, cobrindo desde a identificação de PII até a geração de relatórios executivos de compliance.

Feito utilizando o modelo de LLM llama-3.1-8b-instant, por meio do [Groq Cloud](https://console.groq.com/home). O modelo pode ser alterado via variável de ambiente `LLM_MODEL_ID`.

## Objetivo do Projeto

Demonstrar, de forma prática e aplicada, como a IA pode apoiar processos de governança de dados em ambientes regulados, incluindo:

- Identificação de dados pessoais e financeiros sensíveis (PII)
- Classificação de risco regulatório conforme LGPD
- Definição de políticas de governança de dados
- Mapeamento de linhagem de dados (data lineage)
- Geração de relatórios executivos para áreas de risco, compliance e auditoria

O foco do projeto são dados de crédito, comuns em fintechs, bancos e instituições financeiras.

## Visão Geral da Arquitetura

O sistema é composto por agentes especializados, cada um com uma responsabilidade única, seguindo princípios de separação de responsabilidades, validação defensiva das respostas do LLM e uso da IA como suporte à decisão.

```
Dataset de Crédito (CSV)
  → PII Detector Agent         — identifica colunas sensíveis
  → Data Classifier Agent      — classifica risco e base legal LGPD
  → Lineage Agent              — mapeia linhagem de dados
  → Policy Agent               — define políticas de governança
  → Compliance Reporter Agent  — gera relatório executivo (.md)
```

Para detalhes completos, consulte [docs/architecture.md](docs/architecture.md).

## Estrutura do Projeto

```
agno-data-governance-agent/
├── agents/                  # Agentes especializados de IA
│   ├── __init__.py          # Exporta todos os agentes
│   ├── pii_detector.py
│   ├── data_classifier.py
│   ├── lineage_agent.py
│   ├── policy_agent.py
│   └── compliance_reporter.py
├── pipelines/               # Orquestração do pipeline
│   └── credit_governance_pipeline.py
├── utils/                   # Utilitários compartilhados
│   └── json_parser.py       # Extração e normalização de JSON do LLM
├── tests/                   # Testes unitários e de integração (pytest)
│   ├── conftest.py          # Fixtures compartilhados
│   ├── test_json_parser.py  # Testes unitários (sem API)
│   ├── test_pii_detector.py
│   ├── test_data_classifier.py
│   ├── test_lineage_agent.py
│   ├── test_policy_agent.py
│   └── test_compliance_reporter.py
├── data/                    # Datasets de entrada
│   └── sample_credit_portfolio.csv
├── reports/                 # Relatórios gerados (gitignored)
├── docs/                    # Documentação
│   └── architecture.md
├── .github/workflows/       # CI/CD
│   └── ci.yml               # Lint (Ruff) + testes unitários
├── config.py                # Configuração centralizada
├── pyproject.toml           # Configuração do projeto, deps e ferramentas
├── requirements.txt         # Dependências (alternativa ao uv)
└── .env.example             # Template de variáveis de ambiente
```

## Agentes Implementados

| Agente | Responsabilidade | Saída |
|---|---|---|
| **PII Detector** | Identifica dados sensíveis por coluna (CPF, renda, score, inadimplência) | JSON — lista de classificações por coluna |
| **Data Classifier** | Classifica risco regulatório, base legal LGPD e casos de uso permitidos | JSON — risco, base legal, justificativa |
| **Lineage Agent** | Mapeia origem, transformações, consumidores e riscos dos dados | JSON — linhagem completa |
| **Policy Agent** | Define políticas de retenção, mascaramento e controle de acesso | JSON — políticas estruturadas |
| **Compliance Reporter** | Gera relatório executivo para gestores e auditoria | Markdown — relatório executivo |

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
# Editar .env com suas chaves de API (GROQ_API_KEY obrigatória)

# Instalar dependências (com uv)
uv sync

# Ou com pip
pip install -r requirements.txt
```

### Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GROQ_API_KEY` | Sim | Chave de API do Groq Cloud |
| `TAVILY_API_KEY` | Não | Chave de API do Tavily (busca web) |
| `LLM_MODEL_ID` | Não | Modelo LLM a usar (padrão: `llama-3.1-8b-instant`) |
| `LOG_LEVEL` | Não | Nível de logging (padrão: `INFO`) |

### Executar o pipeline completo

```bash
python pipelines/credit_governance_pipeline.py
```

O pipeline executa os 5 agentes em sequência e salva o relatório de compliance em `reports/compliance_report.md`.

### Executar testes

```bash
# Testes unitários (não requerem API)
pytest tests/test_json_parser.py -v

# Testes de integração (requerem GROQ_API_KEY)
pytest tests/ -m integration -v

# Todos os testes
pytest tests/ -v
```

## Decisões Arquiteturais

- **Validação defensiva**: as respostas dos agentes não assumem saída perfeita do LLM. O parsing e a validação ocorrem via `utils/json_parser.py`.
- **IA como suporte**: agentes apoiam decisões de governança e compliance, não são decisores finais.
- **Configuração centralizada**: model ID, paths e variáveis de ambiente centralizados em `config.py`, sem valores hardcoded nos agentes.
- **Logging estruturado**: logging configurável por nível, substituindo `print()` em todo o projeto.

## Contexto de Uso

Projeto relevante para fintechs, bancos, instituições financeiras e times de dados, risco e compliance, especialmente em ambientes regulados por LGPD, crédito e fraude.

## Possíveis Extensões

- Integração com catálogos de dados
- Validação automática de políticas
- Exportação de relatórios para PDF
- Integração com ferramentas de BI ou Data Governance
- Execução paralela de agentes independentes

## Licença

Projeto desenvolvido para fins educacionais e de portfólio. [Licença MIT](LICENSE).
