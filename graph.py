from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict
from nodes import scrape_node, icp_node, summary_node

class GraphState(TypedDict):
    action: str
    industry: str
    city: str
    state: str
    success: bool
    error: str
    scraped_data: list
    icp_data: dict
    company_name: str
    summary: str

def create_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("scrape", scrape_node)
    workflow.add_node("icp_match", icp_node)
    workflow.add_node("summarize", summary_node)
    
    def route_action(state: GraphState) -> str:
        action = state.get('action', '')
        if action == 'scrape':
            return 'scrape'
        elif action == 'icp_match':
            return 'icp_match'
        elif action == 'summarize':
            return 'summarize'
        return END
    
    workflow.add_node("route", lambda state: state)
    
    workflow.set_entry_point("route")
    
    workflow.add_conditional_edges(
        "route",
        route_action,
        {
            "scrape": "scrape",
            "icp_match": "icp_match", 
            "summarize": "summarize"
        }
    )
    
    workflow.add_edge("scrape", END)
    workflow.add_edge("icp_match", END)
    workflow.add_edge("summarize", END)
    
    return workflow.compile()