from agno.agent import Agent
from agno.models.groq import Groq

from config import LLM_MODEL_ID, get_logger

logger = get_logger(__name__)

PolicyAgent = Agent(
    name="Policy Agent",
    model=Groq(id=LLM_MODEL_ID),
    role="Definir políticas de governança de dados para datasets de crédito",
    instructions="""\
Você é um especialista em governança de dados e LGPD para fintechs.

Você receberá:
- classificação de risco do dataset
- base legal LGPD
- tipos de dados presentes

Defina políticas claras para:
1. Retenção de dados
2. Mascaramento / anonimização
3. Controle de acesso

Retorne SOMENTE um JSON válido no formato:

{
  "retention_policy": "...",
  "masking_policy": "...",
  "access_policy": [
    "..."
  ]
}
""",
)

logger.debug("policy_agent.py carregado")
