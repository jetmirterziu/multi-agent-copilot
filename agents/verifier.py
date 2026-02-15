"""
Verifier Agent - Checks for hallucinations and unsupported claims
"""

from typing import Dict
from .base_agent import BaseAgent
from .prompts import VERIFIER_PROMPT


class VerifierAgent(BaseAgent):
    """Agent that checks for hallucinations and unsupported claims"""
    
    def __init__(self, api_key: str = None):
        super().__init__("Verifier", VERIFIER_PROMPT, api_key)
    
    def execute(self, state: Dict) -> Dict:
        """Execute the verifier agent"""
        trace_log = [self.log("Verifying claims against sources")]
        
        # Prepare research context for verification
        research_context = "\n\n".join([
            f"Source: {note['citation']}\nContent: {note['text']}"
            for note in state['research_notes']
        ])
        
        user_message = f"""Draft to Verify:
{state['draft_output']['full_text']}

Available Research Notes:
{research_context}

Verify this draft against the sources."""
        
        verification_content = self.invoke(user_message)
        
        # Determine if verification passed
        verification_passed = "VERIFICATION: PASS" in verification_content
        
        verification_result = {
            'passed': verification_passed,
            'report': verification_content
        }
        
        # Prepare final output
        final_output = {
            'executive_summary': self._extract_section(state['draft_output']['full_text'], 'Executive Summary'),
            'email': self._extract_section(state['draft_output']['full_text'], 'Email'),
            'action_list': self._extract_section(state['draft_output']['full_text'], 'Action List'),
            'sources': state['research_notes'],
            'full_deliverable': state['draft_output']['full_text'],
            'verification_passed': verification_passed,
            'verification_report': verification_content
        }
        
        trace_log.append(f"Verification: {'PASSED' if verification_passed else 'FAILED'}")
        trace_log.append(f"Sources verified: {len(state['research_notes'])}")
        
        return {
            **state,
            "verification_result": verification_result,
            "final_output": final_output,
            "trace_log": trace_log
        }
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Helper to extract a section from the draft"""
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_name.lower() in line.lower() and ('##' in line or '**' in line or line.isupper()):
                in_section = True
                continue
            elif in_section:
                if line.strip() and ('##' in line or (line.strip().startswith('**') and line.strip().endswith('**'))):
                    break
                section_lines.append(line)
        
        return '\n'.join(section_lines).strip()