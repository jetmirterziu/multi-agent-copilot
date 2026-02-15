"""
Multi-Agent System Orchestrator using LangGraph
Implements: Planner -> Research -> Writer -> Verifier workflow
"""

from typing import TypedDict, List, Dict, Annotated
import operator
from langgraph.graph import StateGraph, END
import os

from .planner import PlannerAgent
from .researcher import ResearchAgent
from .writer import WriterAgent
from .verifier import VerifierAgent


# State definition for the multi-agent system
class AgentState(TypedDict):
    """State passed between agents"""
    user_query: str
    user_goal: str
    plan: str
    research_notes: List[Dict]
    draft_output: Dict
    verification_result: Dict
    final_output: Dict
    trace_log: Annotated[List[str], operator.add]
    

class InsuranceCopilotSystem:
    """Multi-agent copilot system for insurance queries"""
    
    def __init__(self, retriever, api_key: str = None):
        self.retriever = retriever
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize all agents
        self.planner = PlannerAgent(self.api_key)
        self.researcher = ResearchAgent(retriever, self.api_key)
        self.writer = WriterAgent(self.api_key)
        self.verifier = VerifierAgent(self.api_key)
        
        # Build the graph
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("planner", self.planner.execute)
        workflow.add_node("researcher", self.researcher.execute)
        workflow.add_node("writer", self.writer.execute)
        workflow.add_node("verifier", self.verifier.execute)
        
        # Define the workflow edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "writer")
        workflow.add_edge("writer", "verifier")
        workflow.add_edge("verifier", END)
        
        return workflow.compile()
    
    def run(self, user_query: str, user_goal: str) -> Dict:
        """Execute the multi-agent workflow"""
        initial_state = {
            "user_query": user_query,
            "user_goal": user_goal,
            "plan": "",
            "research_notes": [],
            "draft_output": {},
            "verification_result": {},
            "final_output": {},
            "trace_log": ["=== MULTI-AGENT WORKFLOW STARTED ==="]
        }
        
        result = self.graph.invoke(initial_state)
        return result


def create_copilot_system(retriever) -> InsuranceCopilotSystem:
    """Factory function to create the copilot system"""
    return InsuranceCopilotSystem(retriever)