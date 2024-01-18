import requests
import json

from app.database.schemas import ReviewResponseData
from app.logger import get_logger
from app.constants import MISTRAL_API, MODEL, OLLAMA_URL, RUNPOD_API

logger = get_logger("AI")


def ollama_request(user_input):
    prompt = f"""Below are the product reviews in JSON format.
      {user_input}
      Your task is to return JSON response as below format.
      {{
        result: Should I buy the product, true/false?,
        positive: return positive summery in one sentence,
        negative: return negative summery in one sentence,
      }}
    """
    data = {
        "prompt": prompt,
        "model": MODEL,
        "format": "json",
        "stream": False,
        # "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=data)
    json_data = json.loads(response.text)
    return json_data.get("response")


def runpod_request(user_input):
    prompt = f"""Below are the product reviews in JSON format.
      {user_input}
      Your task is to return JSON response as below format.
      {{
        result: Should I buy the product, true/false?,
        positive: return positive summery in one sentence,
        negative: return negative summery in one sentence,
      }}
    """

    payload = json.dumps(
        {"input": {"prompt": prompt}, "policy": {"executionTimeout": 30000}}
    )
    headers = {
        "Authorization": RUNPOD_API,
        "Content-Type": "application/json",
    }
    print(payload)
    response = requests.post(
        "https://api.runpod.ai/v2/l2jvn1isawudjl/runsync", headers=headers, json=payload
    )
    json_data = json.loads(response.text)
    return json_data.get("response")


def mistral_request(user_input):
    prompt = f"""You are a product review analysis bot. Below are the product reviews in JSON format.
      {user_input}
      Your task is to analyze the reviews and Generate a single JSON object response as below format.
      Avoid any additional text or extraneous information; focus solely on the JSON output.
      {{
        result: Should I buy the product, true/false?,
        positive: return positive summery in one sentence,
        negative: return negative summery in one sentence,
      }}
    """
    payload = json.dumps(
        {
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "top_p": 1,
            "stream": False,
            "safe_prompt": False,
            "random_seed": None,
        }
    )
    headers = {
        "Authorization": f"Bearer {MISTRAL_API}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions", headers=headers, data=payload
    )

    json_data = json.loads(response.text)
    logger.info(json_data)
    return json_data.get("choices")[0].get("message").get("content")


def generate_one_time_answer(user_input):
    logger.info(f"Generating AI result")
    json_data = mistral_request(user_input)
    logger.info(f"AI result generated")
    return ReviewResponseData.model_validate_json(json_data)
