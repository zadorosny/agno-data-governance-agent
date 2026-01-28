from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = Groq(id="llama-3.1-8b-instant")

print(">>> policy_agent.py carregado corretamente <<<")

PolicyAgent = Agent(
    name="Policy Agent",
    role="Definir políticas de governança de dados para datasets de crédito",
    model=model,
    instructions="""
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
"""
)
