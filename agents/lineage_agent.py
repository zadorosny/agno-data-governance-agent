from agno.agent import Agent
from agno.models.groq import Groq

from config import LLM_MODEL_ID, get_logger

logger = get_logger(__name__)

LineageAgent = Agent(
    name="Lineage Agent",
    model=Groq(id=LLM_MODEL_ID),
    role="Descrever a linhagem e o fluxo de dados de crédito",
    instructions="""\
Você é um especialista em governança e arquitetura de dados.

Você receberá:
- nome de um dataset
- contexto de uso (ex: crédito, risco)

Descreva a linhagem de dados incluindo:
- origem dos dados
- principais transformações
- sistemas consumidores
- riscos associados

Retorne SOMENTE um JSON válido no formato:

{
  "source": "...",
  "transformations": [...],
  "consumers": [...],
  "risk_points": [...]
}
""",
)

logger.debug("lineage_agent.py carregado")
