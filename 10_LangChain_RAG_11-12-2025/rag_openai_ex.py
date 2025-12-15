
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough

from langchain_openai.embeddings import OpenAIEmbeddings

from langchain_chroma import Chroma

load_dotenv()

loader = TextLoader("product_details.txt", encoding="utf8")
docs = loader.load()
# print(docs[0].page_content)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = splitter.split_documents(docs)

print(type(splits[0]))
print(len(splits))


print(splits[1].page_content) # Print the content of the first split document


vectordb = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory="chroma_db"
)

retriver = vectordb.as_retriever(search_kwargs={"k": 2})

template = """You are a helpful AI assistant.
Use the following pieces of context to answer the question at the end.
{context}
Question: {question}
Answer in a concise manner.
"""

prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o")


chain = ({"context": retriver, "question": RunnablePassthrough()}
        | prompt 
        | llm 
        | StrOutputParser()
        )


response = chain.invoke("suggest products for vacation with kids")
print(response)