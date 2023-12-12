import scrapy
import chromadb
from datetime import datetime
import re
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from chromadb import Documents, EmbeddingFunction, Embeddings
from typing import TypeVar, Union

from constants import MODEL, OLLAMA_URL
from database.schemas import Review

# from database import db_connection

ollama = Ollama(base_url=OLLAMA_URL, model=MODEL)
oembed = OllamaEmbeddings(base_url=OLLAMA_URL, model=MODEL)
client = chromadb.HttpClient(host="127.0.0.1", port=8000)


Embeddable = Documents
D = TypeVar("D", bound=Embeddable, contravariant=True)


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: D) -> Embeddings:
        # embed the documents somehow
        oembed = OllamaEmbeddings(base_url=OLLAMA_URL, model=MODEL)
        return oembed.embed_documents(input)


def get_collection(collection_name):
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=MyEmbeddingFunction(),
    )
    return collection
