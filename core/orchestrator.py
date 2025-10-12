from core.graph import TherapyGraph
from core.storage import MemoryStorage
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from typing import List, Dict, Optional

from services.prompt_store import PromptStore

class TherapyOrchestrator:
    """Главный оркестратор системы"""
    
    def __init__(self, use_memory: bool = True, prompt_store: Optional[PromptStore] = None):
        self.prompt_store = prompt_store or PromptStore()
        self.graph = TherapyGraph(prompt_store=self.prompt_store)
        self.storage = MemoryStorage() if use_memory else None
        self.session_id: Optional[int] = None
        self.messages: List[BaseMessage] = []
        self.user_id = "default"
    
    def start_session(self, user_id: str = "default") -> Optional[int]:
        """Начать новую сессию"""
        self.user_id = user_id
        self.messages = []
        
        if self.storage:
            self.session_id = self.storage.create_session(user_id)
        
        return self.session_id
    
    def process_message(self, user_message: str) -> Dict:
        """Обработать сообщение через граф агентов"""
        
        # Обрабатываем через граф
        result = self.graph.process_message(user_message, self.messages)
        
        # Обновляем историю сообщений
        self.messages = result["messages"]
        
        # Сохраняем в базу данных
        if self.storage and self.session_id:
            self.storage.save_interaction(self.session_id, result)
        
        # Формируем ответ
        return {
            "response": result["specialist_response"],
            "approach": result["current_approach"],
            "confidence": result["confidence"],
            "reasoning": result["reasoning"],
            "insights": result.get("insights", {})
        }
    
    def get_session_insights(self) -> List[Dict]:
        """Получить инсайты текущей сессии"""
        if self.storage and self.session_id:
            return self.storage.get_session_insights(self.session_id)
        return []
    
    def get_session_history(self) -> List[Dict]:
        """Получить историю текущей сессии"""
        if self.storage and self.session_id:
            return self.storage.get_session_history(self.session_id)
        return []

    def refresh_prompts(self) -> None:
        """Reload prompts for all agents from the shared store."""

        if self.prompt_store:
            self.prompt_store.clear_cache()
        self.graph.refresh_prompts()
