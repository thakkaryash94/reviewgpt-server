import os
from dotenv import load_dotenv

load_dotenv()


MODEL = "mistral"  # mistral, llama2
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
RECAPTCHA_TOKEN: str = os.getenv("RECAPTCHA_TOKEN", "")
SENTRY_DSN_URL: str = os.getenv("SENTRY_DSN_URL", "")
OLLAMA_URL: str = os.getenv("OLLAMA_URL", "")
RUNPOD_API: str = os.getenv("RUNPOD_API", "")
MISTRAL_API: str = os.getenv("MISTRAL_API", "")

RECAPTCHA_SITEVERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
