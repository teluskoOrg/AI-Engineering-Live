from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='mistral', messages=[
  {
    'role': 'user',
    'content': 'name one movie for software engineers apart from social network, just the name',
  },
])
print(response['message']['content'])
print(response.message.content)