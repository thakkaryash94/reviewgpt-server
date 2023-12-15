import requests
import json

from app.database.schemas import ReviewResponseData
from .constants import MODEL, OLLAMA_URL


def generate_one_time_answer(user_input):
    prompt = f"""Below are the product reviews in JSON format.
      {user_input}
      Your task is to return only JSON response as below.
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
        "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
    }

    print(f"Generating a result")
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=data, stream=False)
    json_data = json.loads(response.text)
    return ReviewResponseData.model_validate_json(json_data.get("response"))
