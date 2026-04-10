import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

# --- LLM ---
LLM_MODEL_ID: str = os.getenv("LLM_MODEL_ID", "llama-3.1-8b-instant")

# --- Validação de variáveis obrigatórias ---
GROQ_API_KEY: str = os.environ["GROQ_API_KEY"]

# --- Logging ---
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
