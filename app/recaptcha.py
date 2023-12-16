import requests

from app.constants import RECAPTCHA_SITEVERIFY_URL


def recaptcha_verify(payload):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(RECAPTCHA_SITEVERIFY_URL, headers=headers, data=payload)
    data = response.json()
    return data
