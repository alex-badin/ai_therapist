from typing import Dict, List, Optional, Any
from langchain.schema import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models import ChatLiteLLM
from langchain.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import json

# Определяем состояние для LangGraph
class TherapyState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    current_approach: str
    confidence: float
    reasoning: str
    insights: Dict
    session_id: Optional[int]
    user_message: str
    specialist_response: str