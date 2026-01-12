from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

loader = TextLoader("product_details.txt", encoding="utf8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = splitter.split_documents(docs)

print(type(splits[0]))
print(len(splits))
print(splits[1].page_content)

vectordb = Chroma.from_documents(
    documents=splits,
    embedding=GoogleGenerativeAIEmbeddings(model="text-embedding-004"),
    persist_directory="chroma_db_gemini"
)

retriever = vectordb.as_retriever(search_kwargs={"k": 2})

template = """You are a helpful AI assistant.
Use the following pieces of context to answer the question at the end.

Context:
{context}

Question: {question}
Answer in a concise manner.
"""
prompt = PromptTemplate.from_template(template)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = chain.invoke("suggest products for vacation with kids")
print(response)