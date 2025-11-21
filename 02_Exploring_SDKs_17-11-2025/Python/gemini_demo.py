import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

uri = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    "model": "gemini-2.5-flash",
    "messages": [
        {"role": "system", "content": "You are a movie review expert"},
        {
            "role": "user",
            "content": "name one movie for software engineers apart from social network, just the name",
        },
    ],
}

response = requests.post(uri, headers=headers, json=payload)

print(response.text)

data = response.json()
print(data)
