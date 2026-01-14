from langgraph.graph import StateGraph , START, END
from typing import TypedDict


class LoanState(TypedDict):
    income: float
    age: int
    eligible: bool
    max_loan: float
    category: str

def calc_eligibilty(state: LoanState) -> LoanState:
    income = state['income']
    age = state['age']

    eligible = income >= 30000 and 21 <= age <= 65
    max_loan = income * 5 if eligible else 0

    state['eligible'] = eligible
    state['max_loan'] = max_loan

    return state

def label_category(state: LoanState) -> LoanState:
    income = state['income']
    eligible = state['eligible']

    if not eligible:
        category = 'Not Eligible'
    elif income < 50000:
        category = 'Basic'
    elif income < 100000:
        category = 'Premium'
    else:
        category = 'Elite'

    state['category'] = category

    return state

graph = StateGraph(LoanState)

graph.add_node('calc_eligibility', calc_eligibilty)
graph.add_node('label_category', label_category)
graph.add_edge(START, 'calc_eligibility')
graph.add_edge('calc_eligibility', 'label_category')
graph.add_edge('label_category', END)

workflow = graph.compile()

intial_state : LoanState = {
    'income': 5000,
    'age': 30
}

final_state = workflow.invoke(intial_state)

print(final_state)

png = workflow.get_graph().draw_mermaid_png()
with open('loan_eligibility_workflow.png', 'wb') as f:
    f.write(png)