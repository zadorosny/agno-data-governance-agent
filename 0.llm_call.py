from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="user",
    model=Groq(id="llama-3.1-8b-instant"),
    instructions="Responda de forma educada e curta."
)

response = agent.run("Olá, sou o Leo")
print(response)
