import uvicorn
import subprocess

from fastapi import APIRouter, Depends, FastAPI, status
from pydantic import BaseModel, Field

from fastapi.middleware.cors import CORSMiddleware

from typing import Any, TypeVar, Union
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
from sqlalchemy.orm import Session
from chatmodel import generate_one_time_answer
from constants import MODEL
from database import crud, models, schemas
from database.database import get_db, engine
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api")


class ReviewBody(BaseModel):
    url: str = Field(
        examples=[
            "https://www.amazon.in/boAt-Airdopes-161-Playtime-Immersive/product-reviews/B09N7KCNL6",
            "https://www.flipkart.com/boat-airdopes-161-40-hours-playback-asap-charge-10mm-drivers-bluetooth-headset/product-reviews/itm8a7493150ae4a?pid=ACCG6DS7WDJHGWSH&lid=LSTACCG6DS7WDJHGWSH4INU8G&marketplace=FLIPKART",
        ],
    )


# @router.post("/reviews/one-time", response_model=schemas.ReviewResponse)
@router.post("/reviews/one-time")
async def get_one_time_review(body: ReviewBody) -> Any:
    url = body.url
    result: Any
    if "https://www.amazon" in url:
        # Call amazon spider
        result = subprocess.run(
            [
                "scrapy",
                "runspider",
                "./spiders/amazonspider.py",
                "-a",
                f"url={url}",
                "-a",
                f"page=1",
            ],
            capture_output=True,
            text=True,
        )
    if "https://www.flipkart" in url:
        # Call amazon spider
        result = subprocess.run(
            ["scrapy", "runspider", "./spiders/flipkartspider.py", "-a", f"url={url}"],
            capture_output=True,
        )
    if result.stdout:
        # print(result.stdout)
        return {
            "code": status.HTTP_200_OK,
            "message": generate_one_time_answer(result.stdout),
            "success": True,
        }
    else:
        return {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "success": True,
        }


@router.post("/reviews", response_model=schemas.ReviewResponse)
async def get_reviews(body: ReviewBody, db: Session = Depends(get_db)) -> Any:
    url = body.url
    # history = models.History(url=url, is_done=False)
    # db.add(history)
    # db.commit()
    # print(history.id)
    # db.refresh(history)
    if "https://www.amazon" in url:
        # Call amazon spider
        subprocess.run(
            [
                "scrapy",
                "runspider",
                "./spiders/amazonspider.py",
                "-a",
                f"url={url}",
            ]
        )
    if "https://www.flipkart" in url:
        # Call amazon spider
        subprocess.run(
            ["scrapy", "runspider", "./spiders/flipkartspider.py", "-a", f"url={url}"]
        )
    return {
        "code": status.HTTP_200_OK,
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
        oembed = OllamaEmbeddings(base_url="http://127.0.0.1:11434", model=MODEL)
        return oembed.embed_documents(input)


@router.post("/reviews/question")
def post_question(body: QuestionBody, db: Session = Depends(get_db)):
    ollama = Ollama(base_url="http://localhost:11434", model=MODEL)
    oembed = OllamaEmbeddings(base_url="http://localhost:11434", model=MODEL)
    client = chromadb.HttpClient(host="127.0.0.1", port=8000)
    crud.create_history(db=db, history="")

    vectorstore = Chroma(
        client=client,
        collection_name="amz_reviews",
        embedding_function=oembed,
    )
    documents = vectorstore.get().get("documents")

    # Prompt
    # template = """Use the following pieces of context to answer the question at the end.
    # If you don't know the answer, just say that you don't know, don't try to make up an answer.
    # Use three sentences maximum and keep the answer as concise as possible.
    # {context}
    # Question: {question}
    # Helpful Answer:"""
    # QA_CHAIN_PROMPT = PromptTemplate(
    #     input_variables=["context", "question"],
    #     template=template,
    # )
    # qachain = RetrievalQA.from_chain_type(
    #     llm=ollama,
    #     retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
    #     chain_type="stuff",
    #     chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    #     return_source_documents=True,
    # )
    # qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
    # result = qachain({"query": body.question})
    # return result
    chat_model = ChatOllama(
        model=MODEL,
        format="json",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    messages = [
        HumanMessage(content="Below are the reviews of the product. Analyze them"),
        HumanMessage(content="\n".join(documents)),
        HumanMessage(content=body.question),
    ]
    print("\n".join(documents))
    chat_model_response = chat_model(messages)
    return chat_model_response


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
