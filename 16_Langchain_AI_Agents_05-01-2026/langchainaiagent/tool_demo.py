from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage


load_dotenv()

@tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

messages = []

query = "what is the current date and time?"

messages.append(HumanMessage(content=query))

llm = ChatOpenAI(model="gpt-4o")

llm_with_tools = llm.bind_tools([get_current_date_time])

ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

if ai_msg.tool_calls[0]["name"] == "get_current_date_time":
    tool_msg = get_current_date_time.invoke({})
    messages.append(ToolMessage(content=tool_msg, tool_call_id=ai_msg.tool_calls[0]["id"]))
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

print(messages)

# user -> llm
# llm -> tool
# tool -> llm
# llm -> user

# Human Message
# System Message
# AI Message
# Tool Message