from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("{input}")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash"
)

parser = StrOutputParser()

while True:
    value = input("you: ")
    if value.lower() in ["exit", "quit"]:
        break

    chain = prompt | llm | parser

    answer = chain.invoke({"input": value})
    print("AI:", answer)


# Make sure you have install the following package:
  # uv add langchain_google_genai

# Make sure you have GOOGLE_API_KEY in your .env file
  # GOOGLE_API_KEY=your_key_here
 