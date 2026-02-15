"""
Writer Agent - Produces final deliverable using research notes
"""

from typing import Dict
from .base_agent import BaseAgent
from .prompts import WRITER_PROMPT


class WriterAgent(BaseAgent):
    """Agent that produces the final deliverable using research notes"""
    
    def __init__(self, api_key: str = None):
        super().__init__("Writer", WRITER_PROMPT, api_key)
    
    def execute(self, state: Dict) -> Dict:
        """Execute the writer agent"""
        trace_log = [self.log("Creating structured deliverable")]
        
        # Prepare research context
        research_context = "\n\n".join([
            f"Source: {note['citation']}\nContent: {note['text']}"
            for note in state['research_notes']
        ])
        
        user_message = f"""User Query: {state['user_query']}
User Goal: {state['user_goal']}

Execution Plan:
{state['plan']}

Research Notes:
{research_context}

Create a complete deliverable with all required sections."""
        
        draft_content = self.invoke(user_message)
        
        # Parse the draft into sections
        draft_output = {
            'full_text': draft_content,
            'citations_used': [note['citation'] for note in state['research_notes']]
        }
        
        trace_log.append(f"Draft created with {len(draft_content)} characters")
        trace_log.append(f"Citations included: {len(draft_output['citations_used'])}")
        
        return {
            **state,
            "draft_output": draft_output,
            "trace_log": trace_log
        }