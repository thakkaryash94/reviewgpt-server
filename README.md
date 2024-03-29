# ReviewGPT Server

This repo contains source code for server.

## Prerequisite
1. &gt; Python 3.11
2. Neon

## Setup
1. Run `python3 -m venv .venv` to setup development environment
2. Run `pip install -r requirements.txt` to install dependencies
3. Run below command to start the server
```
uvicorn app.main:app --reload --host=0.0.0.0 --port=4000
```
4. Visit http://127.0.0.1:4000/docs for Swagger APIs
5. Run `OLLAMA_HOST=0.0.0.0 OLLAMA_ORIGINS=* ollama serve`
6. Docker build command `docker build -t ogpt-fastapi . --no-cache --platform=linux/amd64`

## DB Migrations
1. Run `alembic revision --autogenerate -m "initial migrations"` to generate migration script
1. Run `alembic upgrade head` to run the migration

Help Links
- [FastAPI](https://fastapi.tiangolo.com)
- [Langchain](https://python.langchain.com/docs/get_started/introduction)
- [Scrapy](https://scrapy.org)
- [Scrapy Playwright](https://github.com/scrapy-plugins/scrapy-playwright)
- [Neon](https://neon.tech/docs/ai/ai-concepts)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [Vector](https://neon.tech/docs/extensions/pgvector)
- [Pydantic](https://docs.pydantic.dev/latest)
