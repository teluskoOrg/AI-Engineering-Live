from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Same model as Spring Boot app: text-embedding-3-small
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="ecom_store",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
