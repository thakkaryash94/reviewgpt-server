import os
from dotenv import load_dotenv

load_dotenv()


MODEL = "llama2"

DATABASE_URL: str = os.getenv("DATABASE_URL", "")

OLLAMA_URL: str = os.getenv("OLLAMA_URL", "")
