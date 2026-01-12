from datetime import datetime
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate

from langchain_classic.agents import create_react_agent, AgentExecutor

load_dotenv()


@tool("get_current_local_time")
def get_current_local_time() -> str:
    """Get the current local date and time (machine local time)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()

llm = ChatOpenAI(model="gpt-4o")


# ReAct prompt (same style as yours)
REACT_PROMPT = PromptTemplate.from_template("""
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


# Subagent: Research Agent (uses ONLY search tool)
research_agent = create_react_agent(llm, [search_tool], REACT_PROMPT)

research_executor = AgentExecutor(
    agent=research_agent,
    tools=[search_tool],
    verbose=True
)

@tool("research_web")
def research_web(query: str) -> str:
    """Use the research subagent to search the web and return a short answer."""
    result = research_executor.invoke({"input": query})
    return result["output"]


# Main agent (Supervisor): has time tool + subagent tool
main_tools = [get_current_local_time, research_web]

supervisor_agent = create_react_agent(llm, main_tools, REACT_PROMPT)

supervisor_executor = AgentExecutor(
    agent=supervisor_agent,
    tools=main_tools,
    verbose=True
)

def chat(query: str) -> str:
    result = supervisor_executor.invoke({"input": query})
    return result["output"]


print(chat("Find which country hosted FIFA 2022 and also tell my current local time."))
