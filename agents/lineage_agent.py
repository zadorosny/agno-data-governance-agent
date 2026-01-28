from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = Groq(id="llama-3.1-8b-instant")

print(">>> lineage_agent.py carregado corretamente <<<")

LineageAgent = Agent(
    name="Lineage Agent",
    role="Descrever a linhagem e o fluxo de dados de crédito",
    model=model,
    instructions="""
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
"""
)
