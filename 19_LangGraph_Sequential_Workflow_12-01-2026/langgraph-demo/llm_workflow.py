from langgraph.graph import StateGraph , START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model_name='gpt-4o')


class JokeState(TypedDict):
    topic: str
    joke: str

def startup_comedian(state: JokeState) -> JokeState:
    prompt = f"Tell me a funny joke about {state['topic']}."
    joke = model.invoke(prompt)
    state['joke'] = joke
    return state

graph = StateGraph(JokeState)

graph.add_node('startup_comedian', startup_comedian)

graph.add_edge(START, 'startup_comedian')
graph.add_edge('startup_comedian', END)

workflow = graph.compile()

intial_state = {
    "topic" : "startups"
}

final_state = workflow.invoke(intial_state)

print(final_state)

png = workflow.get_graph().draw_mermaid_png()
with open('llm_workflow.png', 'wb') as f:
    f.write(png)