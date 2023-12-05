import uvicorn
import subprocess

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, Field


from typing import TypeVar, Union
import chromadb
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores import Chroma
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage

router = APIRouter(prefix="/api")


class ReviewBody(BaseModel):
    url: str = Field(
        examples=[
            "https://www.amazon.in/boAt-Airdopes-161-Playtime-Immersive/product-reviews/B09N7KCNL6",
            "https://www.flipkart.com/boat-airdopes-161-40-hours-playback-asap-charge-10mm-drivers-bluetooth-headset/product-reviews/itm8a7493150ae4a?pid=ACCG6DS7WDJHGWSH&lid=LSTACCG6DS7WDJHGWSH4INU8G&marketplace=FLIPKART",
        ],
    )


@router.post("/reviews")
def get_reviews(body: ReviewBody):
    url = body.url
    if "https://www.amazon" in url:
        # Call amazon spider
        subprocess.run(
            ["scrapy", "runspider", "./spiders/amazonspider.py", "-a", f"url={url}"]
        )
    if "https://www.flipkart" in url:
        # Call amazon spider
        subprocess.run(
            ["scrapy", "runspider", "./spiders/flipkartspider.py", "-a", f"url={url}"]
        )
    return {
        "code": "200",
        "message": "Reviews fetched successfully",
        "success": True,
    }


class QuestionBody(BaseModel):
    question: str


Embeddable = Documents
D = TypeVar("D", bound=Embeddable, contravariant=True)


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: D) -> Embeddings:
        # embed the documents somehow
        oembed = OllamaEmbeddings(base_url="http://127.0.0.1:11434", model="orca2")
        return oembed.embed_documents(input)


@router.post("/reviews/question")
def post_question(body: QuestionBody):
    ollama = Ollama(base_url="http://localhost:11434", model="orca2")
    oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="orca2")
    client = chromadb.HttpClient(host="127.0.0.1", port=8000)

    vectorstore = Chroma(
        client=client,
        collection_name="reviews",
        embedding_function=oembed,
    )
    documents = vectorstore.get().get("documents")

    # Prompt
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    qachain = RetrievalQA.from_chain_type(
        llm=ollama,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        return_source_documents=True,
    )
    qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
    result = qachain({"query": body.question})
    return result
    # chat_model = ChatOllama(
    #   model="orca2",
    #   format="json",
    #   callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    # )
    # messages = [
    # HumanMessage(
    #     content="Below are the reviews of the product. Analyze them"
    # ),
    # HumanMessage(
    #     content='\n'.join(documents)
    # ),
    # ]
    # chat_model_response = chat_model(messages)
    # return chat_model_response


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
