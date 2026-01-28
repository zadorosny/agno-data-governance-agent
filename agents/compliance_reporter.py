from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = Groq(id="llama-3.1-8b-instant")

print(">>> compliance_reporter.py carregado corretamente <<<")

ComplianceReporterAgent = Agent(
    name="Compliance Reporter Agent",
    role="Gerar relatório executivo de compliance LGPD para datasets de crédito",
    model=model,
    instructions="""
Você é um especialista em compliance e governança de dados.

Você receberá:
- classificação de risco do dataset
- base legal LGPD
- políticas de governança definidas
- visão geral da linhagem de dados

Gere um relatório executivo em Markdown contendo:
- Resumo executivo
- Classificação de risco
- Base legal LGPD
- Principais riscos
- Políticas recomendadas
- Próximos passos

Use linguagem clara, objetiva e adequada para público não técnico.
"""
)
