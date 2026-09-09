import requests
import os
from dotenv import load_dotenv

load_dotenv()

jina_api_key = os.getenv("jina_api_key")
if not jina_api_key:
    raise RuntimeError("jina api key not found in .env file")
def get_embeddings(text : str) -> list:
    response = requests.post(
        "https://api.jina.ai/v1/embeddings",
        headers= {
            "Authorization" : f"Bearer {jina_api_key}",
            "Content-Type" : "application/json"
        },
        json = {
            "model" : "jina-embeddings-v2-base-en",
            "input" : [text]
        }
    

    )
    return response.json()["data"][0]["embedding"]
