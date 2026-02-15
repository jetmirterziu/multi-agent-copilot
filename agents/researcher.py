"""
Research Agent - Retrieves grounded information with citations
"""

from typing import Dict, List
from .base_agent import BaseAgent
from .prompts import RESEARCH_PROMPT


class ResearchAgent(BaseAgent):
    """Agent that retrieves grounded information with citations"""
    
    def __init__(self, retriever, api_key: str = None):
        super().__init__("Researcher", RESEARCH_PROMPT, api_key)
        self.retriever = retriever
    
    def execute(self, state: Dict) -> Dict:
        """Execute the research agent"""
        trace_log = [self.log("Starting document retrieval")]
        
        # Parse plan to extract research queries
        plan_lines = state['plan'].split('\n')
        research_queries = []
        
        for line in plan_lines:
            if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-')):
                research_queries.append(line.strip())
        
        # If no queries extracted, use the original user query
        if not research_queries:
            research_queries = [state['user_query']]
        
        # Perform retrieval for each query
        all_research_notes = []
        seen_chunks = set()
        
        trace_log.append(f"Executing {len(research_queries)} research queries")
        
        for query in research_queries[:5]:  # Limit to 5 queries max
            results = self.retriever.search(query, k=3)
            
            for result in results:
                chunk_key = f"{result['document']}_{result['chunk_id']}"
                if chunk_key not in seen_chunks:
                    all_research_notes.append({
                        'text': result['text'],
                        'citation': result['citation'],
                        'document': result['document'],
                        'chunk_id': result['chunk_id'],
                        'relevance': result['relevance_score'],
                        'query': query
                    })
                    seen_chunks.add(chunk_key)
        
        trace_log.append(f"Retrieved {len(all_research_notes)} unique document chunks")
        trace_log.append(f"Documents used: {', '.join(set(note['document'] for note in all_research_notes))}")
        
        return {
            **state,
            "research_notes": all_research_notes,
            "trace_log": trace_log
        }