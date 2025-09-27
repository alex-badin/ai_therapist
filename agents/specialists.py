from typing import List
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from langchain_community.chat_models import ChatLiteLLM
from agents.prompts import (
    ROUTER_PROMPT, DBT_PROMPT, IFS_PROMPT, 
    TRE_PROMPT, MEMORY_PROMPT
)
from agents.base import TherapyState
from config import LITELLM_CONFIG
import json

class BaseAgent:
    """Базовый класс агента с LiteLLM"""
    
    def __init__(self, system_prompt: str, name: str):
        self.llm = ChatLiteLLM(**LITELLM_CONFIG)
        self.system_prompt = system_prompt
        self.name = name
    
    def process(self, user_message: str, context: List[BaseMessage] = None) -> str:
        messages = [SystemMessage(content=self.system_prompt)]
        
        if context:
            # Добавляем последние 5 сообщений для контекста
            messages.extend(context[-5:])
        
        messages.append(HumanMessage(content=user_message))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Ошибка в {self.name}: {e}")
            return f"Ошибка обработки: {str(e)}"

class RouterAgent(BaseAgent):
    """Агент маршрутизации"""
    
    def __init__(self):
        super().__init__(ROUTER_PROMPT, "Router")
    
    def route(self, state: TherapyState) -> TherapyState:
        """Определяет подходящий терапевтический подход"""
        user_message = state["user_message"]
        
        response = self.process(user_message, state.get("messages", []))
        
        try:
            # Парсим JSON ответ
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            
            data = json.loads(response.strip())
            
            state["current_approach"] = data.get("approach", "DBT")
            state["confidence"] = data.get("confidence", 0.5)
            state["reasoning"] = data.get("reasoning", "")
            
        except Exception as e:
            print(f"Ошибка парсинга роутера: {e}")
            state["current_approach"] = "DBT"
            state["confidence"] = 0.5
            state["reasoning"] = "Использую DBT по умолчанию"
        
        return state

class DBTAgent(BaseAgent):
    def __init__(self):
        super().__init__(DBT_PROMPT, "DBT Specialist")
    
    def respond(self, state: TherapyState) -> TherapyState:
        response = self.process(state["user_message"], state.get("messages", []))
        state["specialist_response"] = response
        return state

class IFSAgent(BaseAgent):
    def __init__(self):
        super().__init__(IFS_PROMPT, "IFS Specialist")
    
    def respond(self, state: TherapyState) -> TherapyState:
        response = self.process(state["user_message"], state.get("messages", []))
        state["specialist_response"] = response
        return state

class TREAgent(BaseAgent):
    def __init__(self):
        super().__init__(TRE_PROMPT, "TRE Specialist")
    
    def respond(self, state: TherapyState) -> TherapyState:
        response = self.process(state["user_message"], state.get("messages", []))
        state["specialist_response"] = response
        return state

class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(MEMORY_PROMPT, "Memory")
    
    def extract(self, state: TherapyState) -> TherapyState:
        # Создаем контекст для анализа
        context = f"""
        Сообщение пользователя: {state['user_message']}
        Подход: {state['current_approach']}
        Ответ специалиста: {state['specialist_response']}
        """
        
        response = self.process(context)
        
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            
            state["insights"] = json.loads(response.strip())
        except:
            state["insights"] = {
                "insights": [],
                "patterns": [],
                "keywords": []
            }
        
        return state