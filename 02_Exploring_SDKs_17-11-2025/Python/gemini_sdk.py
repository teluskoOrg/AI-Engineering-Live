from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="name one movie for software engineers apart from social network, just the name"
)
print(response.text)