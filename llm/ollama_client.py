import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL"
)

MODEL = os.getenv(
    "MODEL_NAME"
)


def generate_response(system_prompt, user_prompt):

    payload = {
        "model": MODEL,
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:

        return f"AI Error : {str(e)}"