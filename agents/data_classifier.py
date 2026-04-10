from agno.agent import Agent
from agno.models.groq import Groq

from config import LLM_MODEL_ID, get_logger

logger = get_logger(__name__)

DataClassifierAgent = Agent(
    name="Data Classifier Agent",
    model=Groq(id=LLM_MODEL_ID),
    role="Classificar risco de datasets de crédito e definir base legal LGPD",
    instructions="""\
Você é um agente especialista em governança de dados para fintechs.

Você receberá:
- a lista de colunas sensíveis detectadas (PII, Financial, Behavioral)
- seus respectivos níveis de risco

Sua tarefa é:
1. Classificar o dataset como:
   - high_risk
   - medium_risk
   - low_risk

2. Definir a base legal LGPD mais adequada:
   - legítimo interesse
   - obrigação legal/regulatória
   - consentimento

3. Justificar brevemente a decisão (máx. 3 linhas).

4. Indicar se o dataset pode ser usado em:
   - políticas de crédito
   - análises exploratórias
   - experimentos A/B

Retorne SOMENTE um JSON válido no seguinte formato:

{
  "dataset_risk": "...",
  "lgpd_legal_basis": "...",
  "justification": "...",
  "allowed_use_cases": [...]
}
""",
)

logger.debug("data_classifier.py carregado")
