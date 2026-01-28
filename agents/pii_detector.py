from agno.agent import Agent
from agno.models.groq import Groq
#from agno.models.message import Message

from dotenv import load_dotenv
load_dotenv()

model = Groq(id="llama-3.1-8b-instant")

print(">>> pii_detector.py carregado corretamente <<<")

PIIDetectorAgent = Agent(
    name="PII Detector Agent",
    model=model,
    role="Detectar dados pessoais e financeiros sensíveis em datasets de crédito",
    instructions="""
Você é um agente especializado em governança de dados para fintechs.

Sua tarefa é analisar:
- esquema do dataset (nomes das colunas)
- amostras de linhas

Identifique dados sensíveis, incluindo:
- CPF
- renda (monthly_income)
- limite de crédito
- score de crédito
- indicadores de inadimplência
- identificadores de clientes

Para cada coluna sensível, retorne SOMENTE um JSON válido
no formato de lista, sem explicações adicionais.

Cada item deve conter:
- column
- data_type (PII, Financial, Behavioral)
- pii_category
- risk_level (high, medium, low)
- confidence (0 a 1)
"""
)
