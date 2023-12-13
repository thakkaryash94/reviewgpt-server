import json
import requests
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage
from .constants import MODEL


# def chat(prompt_message):
#     r = requests.post(
#         f"{OLLAMA_URL}/api/generate",
#         json={"model": MODEL, "prompt": prompt_message, "stream": False},
#     )
#     r.raise_for_status()

#     for line in r.iter_lines():
#         body = json.loads(line)
#         return body.get("response", "")


def generate_one_time_answer(user_input):
    messages = [
        HumanMessage(content="Below are the product reviews in JSON format"),
        HumanMessage(content=user_input),
        HumanMessage(
            content="Now, considering the reviews, tell me whether should I buy the product or not in brief answer?"
        ),
    ]
    chat_model = ChatOllama(model=MODEL, format="json")
    chat_model_response = chat_model(messages)
    return chat_model_response.content

    # qa_chain = RetrievalQA.from_chain_type(
    # chat_model,
    # retriever=vectorstore.as_retriever(),
    # chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    # )
    # question = "What are the approaches to Task Decomposition?"
    # result = qa_chain({"query": question})

    # return chat(
    #     f"Below is json reviews of the product. \n{user_input}\nShould I buy this product, answer in yes or no only?"
    # )
