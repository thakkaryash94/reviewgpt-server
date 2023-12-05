# ReviewGPT Server

This repo contains source code for server.

## Prerequisite
1. &gt; Python 3.11
2. ChromaDB

## Setup
1. Run `python3 -m venv .venv` to setup development environment
2. Run `pip install -r requirements.txt` to install dependencies
3. Run below command to start the server
```
uvicorn main:app --reload --port=5000
```
4. Visit http://127.0.0.1:5000/docs for Swagger APIs

Help Links
- [FastAPI](https://fastapi.tiangolo.com)
- [Langchain](https://python.langchain.com/docs/get_started/introduction)
- [Scrapy](https://scrapy.org)
- [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright)
