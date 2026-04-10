# Arquitetura do Sistema

## Visão Geral

O sistema segue uma arquitetura de **pipeline sequencial de agentes especializados**, onde cada agente tem uma responsabilidade única e passa sua saída para o próximo na cadeia.

```
┌─────────────────┐
│  Dataset (CSV)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  PII Detector   │  → Identifica colunas sensíveis (PII, Financial, Behavioral)
└────────┬────────┘
         ▼
┌─────────────────┐
│ Data Classifier │  → Classifica risco do dataset e base legal LGPD
└────────┬────────┘
         ▼
┌─────────────────┐
│ Lineage Agent   │  → Mapeia origem, transformações e consumidores dos dados
└────────┬────────┘
         ▼
┌─────────────────┐
│  Policy Agent   │  → Define políticas de retenção, mascaramento e acesso
└────────┬────────┘
         ▼
┌──────────────────────┐
│ Compliance Reporter  │  → Gera relatório executivo em Markdown
└──────────┬───────────┘
           ▼
     ┌───────────┐
     │  Relatório │
     │   (.md)    │
     └───────────┘
```

## Estrutura de Diretórios

```
agno-data-governance-agent/
├── agents/              # Definições dos agentes especializados
│   ├── __init__.py      # Exporta todos os agentes
│   ├── pii_detector.py
│   ├── data_classifier.py
│   ├── lineage_agent.py
│   ├── policy_agent.py
│   └── compliance_reporter.py
├── pipelines/           # Orquestração do pipeline
│   └── credit_governance_pipeline.py
├── utils/               # Utilitários compartilhados
│   └── json_parser.py   # Extração e normalização de JSON do LLM
├── tests/               # Testes (unitários e integração)
├── data/                # Datasets de entrada
├── reports/             # Relatórios gerados (gitignored)
├── docs/                # Documentação
└── config.py            # Configuração centralizada
```

## Princípios de Design

1. **Separação de responsabilidades**: cada agente tem um escopo único e bem definido.
2. **Validação defensiva**: respostas do LLM são parseadas e validadas antes de uso.
3. **IA como suporte**: agentes apoiam decisões de governança, não substituem controles humanos.
4. **Configuração centralizada**: model IDs, paths e variáveis de ambiente em `config.py`.

## Stack Tecnológica

| Componente | Tecnologia |
|---|---|
| Framework de agentes | [Agno](https://github.com/agno-agi/agno) |
| LLM | Llama 3.1 8B (via Groq Cloud) |
| Manipulação de dados | Pandas |
| Testes | Pytest |
| Gerenciador de pacotes | uv |

## Comunicação entre Agentes

Cada agente recebe input via `Message(role="user", content=json_string)` e retorna texto (JSON ou Markdown). A camada de orquestração (`pipelines/`) é responsável por:

- Serializar payloads em JSON
- Extrair e validar JSON das respostas (`utils/json_parser.py`)
- Encadear a saída de um agente como entrada do próximo
