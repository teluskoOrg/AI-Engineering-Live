import requests
from openai import OpenAI

client = OpenAI()


def generate_image(prompt: str) -> bytes:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="standard",
        response_format="url"
    )
    image_url = response.data[0].url
    return requests.get(image_url).content
