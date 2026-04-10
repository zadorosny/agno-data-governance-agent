from agno.agent import Agent
from agno.models.groq import Groq

from config import LLM_MODEL_ID, get_logger

logger = get_logger(__name__)

ComplianceReporterAgent = Agent(
    name="Compliance Reporter Agent",
    model=Groq(id=LLM_MODEL_ID),
    role="Gerar relatório executivo de compliance LGPD para datasets de crédito",
    instructions="""\
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
""",
)

logger.debug("compliance_reporter.py carregado")
