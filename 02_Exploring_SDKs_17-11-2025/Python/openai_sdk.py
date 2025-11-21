from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="name one movie for software engineers apart from social network, just the name"
)

print(response.output_text)