import requests

uri = "http://localhost:11434/api/chat"

payload = {
    "model": "mistral",   
    "messages": [
        {
            "role": "user",
            "content": "name one movie for software engineers apart from social network, just the name"
        }
    ],
    "stream": False        
}

response = requests.post(uri, json=payload)
response.raise_for_status()   

print(response.json()["message"]["content"])
