from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

@tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()

llm = ChatOpenAI(model="gpt-4o")

tools = [get_current_date_time, search_tool]

llm_with_tools = llm.bind_tools(tools)

def chat(query:str) -> str:
    messages = []
    messages.append(HumanMessage(content=query))

    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        # print(messages)

        if not ai_msg.tool_calls:
            return ai_msg.content
        
        for tc in ai_msg.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]

            tool_fn = next(t for t in tools if t.name == tool_name)
            tool_msg = tool_fn.invoke(tool_args)
            messages.append(ToolMessage(content=tool_msg, tool_call_id=tc["id"]))
        

# response = chat("who is the founder of Telusko? ")
response = chat("Current time in the country where messi visited in Dec 2025 ")
print(response)