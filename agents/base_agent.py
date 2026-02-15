"""
Base agent class with common functionality
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, system_prompt: str, api_key: str = None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            temperature=0
        )
    
    def invoke(self, user_message: str) -> str:
        """Invoke the LLM with system and user messages"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message)
        ]
        response = self.llm.invoke(messages)
        return response.content
    
    def log(self, message: str) -> str:
        """Create a log entry for this agent"""
        return f"\n=== {self.name.upper()} AGENT ===\n{message}"