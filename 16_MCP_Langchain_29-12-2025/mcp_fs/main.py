
import asyncio
import platform
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

MCP_FOLDER = r"C:\\Users\\navin\\OneDrive\\Desktop\\mcp_folder"

def npx_command():
    return "npx" if platform.system() != "Windows" else "npx.cmd"

async def chat(query):
    Client = MultiServerMCPClient({
        "filesystem": {
            "transport": "stdio",
            "command": npx_command(),
            "args": ["-y", "@modelcontextprotocol/server-filesystem", MCP_FOLDER]

        },
        "telusko":{
            "transport": "sse",
            "url": "http://localhost:8000/sse"
        }
    })

    tools = await Client.get_tools()

    lms = ChatOpenAI(model="gpt-4o")
    llm_with_tools = lms.bind_tools(tools)

    messages = []

    messages.append(SystemMessage(content=f"You are an expret file system assistant. All file operations are in {MCP_FOLDER}"))
    messages.append(HumanMessage(content=query))

    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            return ai_msg.content
        
        for tc in ai_msg.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            tool_fn = next(tool for tool in tools if tool.name == tool_name)

            tool_result = await tool_fn.ainvoke(tool_args)
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tc["id"]))

prompt = "Current time in the country where messi visited in Dec 2025"

response = asyncio.run(chat(prompt))


print(response)