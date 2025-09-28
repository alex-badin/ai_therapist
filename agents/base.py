from typing import Dict, List, Optional
from typing import TypedDict, Annotated
from langchain.schema import BaseMessage
import operator

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