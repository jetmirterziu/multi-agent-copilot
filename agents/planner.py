"""
Planner Agent - Decomposes tasks and creates execution plans
"""

from typing import Dict
from .base_agent import BaseAgent
from .prompts import PLANNER_PROMPT


class PlannerAgent(BaseAgent):
    """Agent that decomposes the task and creates an execution plan"""
    
    def __init__(self, api_key: str = None):
        super().__init__("Planner", PLANNER_PROMPT, api_key)
    
    def execute(self, state: Dict) -> Dict:
        """Execute the planner agent"""
        trace_log = [self.log("Starting task decomposition")]
        
        user_message = f"""User Query: {state['user_query']}
User Goal: {state['user_goal']}

Create an execution plan for this task."""
        
        plan = self.invoke(user_message)
        
        num_steps = len(plan.split('\n'))
        trace_log.append(f"Plan created with {num_steps} steps")
        trace_log.append(f"Plan preview: {plan[:200]}...")
        
        return {
            **state,
            "plan": plan,
            "trace_log": trace_log
        }