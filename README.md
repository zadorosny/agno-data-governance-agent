# agno-data-governance-agent

Sistema multiagente baseado em IA para governança de dados sensíveis, com foco em datasets de crédito e portfólio financeiro, aplicando princípios da LGPD, risco regulatório e boas práticas de compliance.

O projeto simula como fintechs, bancos e instituições financeiras podem utilizar agentes de IA para apoiar decisões de governança de dados, sem substituir controles humanos, cobrindo desde a identificação de PII até a geração de relatórios executivos de compliance.

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

Dataset de Crédito  
→ PII Detector Agent  
→ Data Classifier Agent (LGPD / Risco)  
→ Lineage Agent (Linhagem de Dados)  
→ Policy Agent (Políticas de Governança)  
→ Compliance Reporter Agent (Relatório Executivo)

## Agentes Implementados

PII Detector Agent  
Responsável por identificar dados sensíveis por coluna, como CPF, identificadores de clientes, dados financeiros (renda, limite de crédito, score) e indicadores comportamentais (inadimplência).  
Saída: classificação estruturada contendo tipo do dado, categoria, nível de risco e grau de confiança.

Data Classifier Agent  
Classifica o dataset como um todo, definindo nível de risco regulatório, base legal LGPD aplicável e casos de uso permitidos.  
Objetivo: apoiar decisões sobre uso, tratamento e restrições do dataset.

Lineage Agent  
Descreve a linhagem dos dados, incluindo origem, transformações aplicadas, sistemas consumidores e pontos críticos de risco.  
Uso típico: auditorias, análises de impacto e governança de dados.

Policy Agent  
Traduz risco regulatório em políticas acionáveis, como política de retenção, estratégias de mascaramento ou anonimização e controle de acesso por perfil.  
Saída: políticas estruturadas prontas para aplicação operacional.

Compliance Reporter Agent  
Gera um relatório executivo em Markdown, voltado para gestores, áreas de risco, compliance e auditoria.  
O relatório inclui resumo executivo, classificação de risco, base legal LGPD, principais riscos, políticas recomendadas e próximos passos, simulando entregáveis reais de ambientes regulados.

## Como Executar

Instalar dependências:

pip install -r requirements.txt```

Executar agentes individualmente (scripts executáveis e documentação viva):

python test_pii_detector.py
python test_data_classifier.py
python test_lineage_agent.py
python test_policy_agent.py
python test_compliance_reporter.py

Executar o pipeline completo de governança:

python pipelines/credit_governance_pipeline.py

## Decisões Arquiteturais

As respostas dos agentes não assumem saída perfeita do LLM. O parsing e a validação ocorrem na camada de consumo.
A IA atua como suporte à governança e compliance, não como decisora final.
Os arquivos test_*.py funcionam como exemplos de uso, testes de integração e documentação executável.

## Contexto de Uso

Projeto relevante para fintechs, bancos, instituições financeiras e times de dados, risco e compliance, especialmente em ambientes regulados por LGPD, crédito e fraude.

## Possíveis Extensões

Integração com catálogos de dados
Validação automática de políticas
Exportação de relatórios para PDF
Integração com ferramentas de BI ou Data Governance

## Licença

Projeto desenvolvido para fins educacionais e de portfólio.


