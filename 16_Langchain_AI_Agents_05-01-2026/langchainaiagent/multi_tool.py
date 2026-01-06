from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

load_dotenv()

@tool("get_current_local_time")
def get_current_local_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4o")

tools = [get_current_local_time, search_tool]

prompt = PromptTemplate.from_template("""
You are an AI assistant that can use tools.

TOOLS:
{tools}

IMPORTANT:
- Always follow the format exactly.
- Always end with: Final Answer: ...

Format:

Question: {input}
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: the input to the action
Observation: the tool result
... (repeat Thought/Action/Action Input/Observation if needed)
Thought: I now know the final answer
Final Answer: the final answer

Begin!

Question: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

def chat(query: str) -> str:
    result = agent_executor.invoke({"input": query})
    return result["output"]

response = chat("Current time in the country where messi visited in Dec 2025 ")
print(response)