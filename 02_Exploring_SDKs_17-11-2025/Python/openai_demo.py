
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

uri = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4o",
    "messages": [
        {"role": "user", "content": "name one movie for software engineers apart from social network, just the name"}
    ]
}


response = requests.post(uri, headers=headers, json=payload)

print(response.json()["choices"][0]["message"]["content"])