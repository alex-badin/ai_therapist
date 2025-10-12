from langgraph.graph import StateGraph, END
from agents import prompts as prompt_defaults
from agents.specialists import (
    RouterAgent, DBTAgent, IFSAgent, TREAgent, MemoryAgent,
    TherapyState
)
from langchain.schema import HumanMessage, AIMessage
from typing import Dict, List

class TherapyGraph:
    """Граф обработки сообщений через агентов"""
    
    def __init__(self, prompt_store=None):
        self.prompt_store = prompt_store
        self._default_prompts = {
            "router": prompt_defaults.ROUTER_PROMPT,
            "dbt": prompt_defaults.DBT_PROMPT,
            "ifs": prompt_defaults.IFS_PROMPT,
            "tre": prompt_defaults.TRE_PROMPT,
            "memory": prompt_defaults.MEMORY_PROMPT,
        }
        self._active_prompts = self._collect_prompts()

        # Инициализация агентов
        self.router = RouterAgent(self._active_prompts["router"])
        self.dbt_agent = DBTAgent(self._active_prompts["dbt"])
        self.ifs_agent = IFSAgent(self._active_prompts["ifs"])
        self.tre_agent = TREAgent(self._active_prompts["tre"])
        self.memory_agent = MemoryAgent(self._active_prompts["memory"])
        
        # Построение графа
        self.workflow = StateGraph(TherapyState)
        
        # Добавляем узлы
        self.workflow.add_node("router", self.router.route)
        self.workflow.add_node("dbt", self.dbt_agent.respond)
        self.workflow.add_node("ifs", self.ifs_agent.respond)
        self.workflow.add_node("tre", self.tre_agent.respond)
        self.workflow.add_node("memory", self.memory_agent.extract)
        
        # Устанавливаем точку входа
        self.workflow.set_entry_point("router")
        
        # Добавляем условные переходы
        self.workflow.add_conditional_edges(
            "router",
            self.route_to_specialist,
            {
                "DBT": "dbt",
                "IFS": "ifs",
                "TRE": "tre"
            }
        )
        
        # Все специалисты ведут к памяти
        self.workflow.add_edge("dbt", "memory")
        self.workflow.add_edge("ifs", "memory")
        self.workflow.add_edge("tre", "memory")
        
        # Память ведет к концу
        self.workflow.add_edge("memory", END)
        
        # Компилируем граф
        self.app = self.workflow.compile()

    def route_to_specialist(self, state: TherapyState) -> str:
        """Определяет, к какому специалисту направить"""
        return state["current_approach"]

    def refresh_prompts(self) -> None:
        """Reload prompts from the store and update agent system prompts."""

        self._active_prompts = self._collect_prompts()
        self.router.set_system_prompt(self._active_prompts["router"])
        self.dbt_agent.set_system_prompt(self._active_prompts["dbt"])
        self.ifs_agent.set_system_prompt(self._active_prompts["ifs"])
        self.tre_agent.set_system_prompt(self._active_prompts["tre"])
        self.memory_agent.set_system_prompt(self._active_prompts["memory"])

    def process_message(self, user_message: str, messages: List = None) -> Dict:
        """Обрабатывает сообщение пользователя через граф"""
        
        # Подготавливаем начальное состояние
        initial_state = {
            "messages": messages or [],
            "user_message": user_message,
            "current_approach": None,
            "confidence": 0,
            "reasoning": "",
            "insights": {},
            "session_id": None,
            "specialist_response": ""
        }
        
        # Запускаем граф
        result = self.app.invoke(initial_state)

        # Добавляем сообщения в историю
        result["messages"].append(HumanMessage(content=user_message))
        result["messages"].append(AIMessage(content=result["specialist_response"]))

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _collect_prompts(self) -> Dict[str, str]:
        if self.prompt_store:
            return self.prompt_store.get_all(self._default_prompts)
        return dict(self._default_prompts)
