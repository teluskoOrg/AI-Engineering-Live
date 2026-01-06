
from fastmcp import FastMCP
from datetime import datetime

from langchain_community.tools import DuckDuckGoSearchRun

mcp = FastMCP("TelsukoMCPServer")

search_tool = DuckDuckGoSearchRun()

@mcp.tool()
def get_current_local_time() -> str:
    """Get the current local time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool()
def web_serach(query: str) -> str:
    """Search the web using DuckDuckGo."""
    return search_tool.run(query)

mcp.run(transport="sse", host="localhost", port=8000)