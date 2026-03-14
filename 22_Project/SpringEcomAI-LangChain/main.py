from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import products, orders, chatbot

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpringEcomAI - Python LangChain Version")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(chatbot.router)


@app.get("/")
def root():
    return {"message": "SpringEcomAI Python API is running!"}
