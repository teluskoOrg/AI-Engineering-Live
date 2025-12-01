
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
load_dotenv()


prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder("history"),"{input}"])

llm = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()

chain = prompt | llm | parser

store = {}
session_id = "naveen_session_1"

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)



while True:
    value = input("You:")
    if(value.lower() in ["exit","quit"]):
        break

    answer = chain_with_history.invoke({"input":value},
                        config={"configurable": {"session_id": session_id}})
    
    print("AI:", answer)
