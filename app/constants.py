import os
from dotenv import load_dotenv

load_dotenv()


# MODEL = "mistral"
MODEL = "llama2"
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
OLLAMA_URL: str = os.getenv("OLLAMA_URL", "")
RECAPTCHA_TOKEN: str = os.getenv("RECAPTCHA_TOKEN", "")

RECAPTCHA_SITEVERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
