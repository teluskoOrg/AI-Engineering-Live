# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_community.tools import YouTubeSearchTool

# search_tool = DuckDuckGoSearchRun()
# yt_tool = YouTubeSearchTool()

# response = search_tool.invoke("top news in cricket today")
# response1 = yt_tool.invoke("Best java and python videos (from telusko)")

# print(response1)
# print(yt_tool.name)
# print(yt_tool.description)
# print(yt_tool.args)

# Yt tool and DuckDuckGoSearchRun tool above


from langchain_core.tools import tool
from datetime import datetime

@tool("get_current_date_time")
def get_current_date_time():
    """Get the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

result = get_current_date_time.invoke({})
print(f"Current date and time: {result}")