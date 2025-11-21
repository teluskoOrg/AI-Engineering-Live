from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

words = ["cat", "Dog", "Fish", "laptop", "Java", "Python", "King", "Queen", "Apple", "Banana", "Mars", "Kitty"]

for word in words:
    response = client.embeddings.create(
        input=word,
        model="text-embedding-3-large",
        dimensions=2
    )

    embedding = response.data[0].embedding
    print(f"{word} = ({embedding[0]:.6f}, {embedding[1]:.6f})")