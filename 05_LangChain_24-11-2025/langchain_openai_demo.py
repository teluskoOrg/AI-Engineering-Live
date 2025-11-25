
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("{input}")

llm = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()


while True:
    value = input("you: ")
    if value.lower() in ["exit", "quit"]:
        break
    chain = prompt | llm | parser

    answer = chain.invoke({"input":value})
    print("AI: "+answer)