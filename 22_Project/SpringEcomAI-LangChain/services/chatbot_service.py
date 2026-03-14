import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from config.vector_store import vector_store

llm = ChatOpenAI(model="gpt-4o")

chat_history: list = []
MAX_HISTORY = 20

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "chatbot-rag-prompt.st"


def _load_prompt(context: str, user_query: str) -> str:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return template.replace("{context}", context).replace("{userQuery}", user_query)


def get_bot_response(user_query: str) -> str:
    global chat_history

    docs = vector_store.similarity_search(user_query, k=5)
    context = "\n".join([doc.page_content for doc in docs])

    final_prompt = _load_prompt(context, user_query)

    messages = [{"role": "system", "content": final_prompt}]
    for msg in chat_history[-MAX_HISTORY:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_query})

    response = llm.invoke(messages)
    reply = response.content

    chat_history.append({"role": "user", "content": user_query})
    chat_history.append({"role": "assistant", "content": reply})

    if len(chat_history) > MAX_HISTORY * 2:
        chat_history = chat_history[-(MAX_HISTORY * 2):]

    return reply
