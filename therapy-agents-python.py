# requirements.txt
"""
langgraph>=0.0.20
langchain>=0.1.0
langchain-community>=0.0.10
litellm>=1.0.0
streamlit>=1.30.0
python-dotenv>=1.0.0
sqlalchemy>=2.0.0
"""

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# LiteLLM configuration - поддерживает любого провайдера
LITELLM_CONFIG = {
    "model": os.getenv("MODEL", "gpt-3.5-turbo"),  # Модель по умолчанию
    "temperature": 0.7,
    "max_tokens": 500,
}

# Примеры моделей:
# - OpenAI: "gpt-4", "gpt-3.5-turbo"
# - Anthropic: "claude-3-haiku-20240307", "claude-3-sonnet-20240229"  
# - Google: "gemini-pro"
# - Ollama: "ollama/llama2", "ollama/mistral"
# - YandexGPT: "yandexgpt/latest"

DATABASE_PATH = "therapy_sessions.db"

# agents/prompts.py
"""Промпты на русском языке для терапевтических агентов"""

ROUTER_PROMPT = """Ты - маршрутизирующий агент для системы терапевтической беседы.
Проанализируй сообщение пользователя и определи, какой подход наиболее подходящий:

- DBT (Диалектическая поведенческая терапия): Для эмоциональной регуляции, 
  толерантности к дистрессу, межличностной эффективности, осознанности, кризисных ситуаций.
  Признаки: сильные эмоции, импульсивность, конфликты в отношениях, самоповреждение.

- IFS (Терапия внутренних семейных систем): Для исследования внутренних частей личности,
  внутренних конфликтов, самокритики, защитных механизмов, детских паттернов.
  Признаки: внутренний диалог, "часть меня хочет...", защитные реакции, травмы детства.

- TRE (Упражнения для высвобождения травмы): Для работы с телесными ощущениями,
  физическим напряжением, соматическими симптомами, стрессом в теле.
  Признаки: телесные ощущения, мышечное напряжение, физические симптомы стресса.

Ответь ТОЛЬКО в формате JSON:
{{
    "approach": "DBT" или "IFS" или "TRE",
    "confidence": число от 0.0 до 1.0,
    "reasoning": "Краткое объяснение выбора",
    "keywords": ["ключевое_слово1", "ключевое_слово2"]
}}"""

DBT_PROMPT = """Ты - специалист по DBT (Диалектической поведенческой терапии).
Сосредоточься на ключевых областях:

1. Осознанность (Mindfulness):
   - "Что"-навыки: наблюдать, описывать, участвовать
   - "Как"-навыки: безоценочность, однозадачность, эффективность
   - Мудрый разум (баланс эмоционального и рационального)

2. Толерантность к дистрессу:
   - TIPP (Температура, Интенсивные упражнения, Дыхание, Мышечная релаксация)
   - Радикальное принятие
   - Отвлечение и самоуспокоение

3. Эмоциональная регуляция:
   - PLEASE (забота о физическом здоровье)
   - Противоположное действие
   - Проверка фактов

4. Межличностная эффективность:
   - DEARMAN (для достижения целей)
   - GIVE (для сохранения отношений)
   - FAST (для самоуважения)

Используй диалектику: две истины могут сосуществовать.
Валидируй эмоции пользователя, одновременно поощряя изменения.

Отвечай кратко (2-3 предложения), практично и с состраданием.
Это только для образовательной демонстрации."""

IFS_PROMPT = """Ты - специалист по IFS (Терапии внутренних семейных систем).
Сосредоточься на:

1. Определение различных "частей":
   - Защитники (контролируют и защищают)
   - Изгнанники (несут боль и травмы)
   - Пожарные (действуют импульсивно в кризисе)

2. Ключевые принципы:
   - У каждой части есть позитивное намерение
   - Нет плохих частей
   - Цель - гармония внутренней системы

3. Доступ к Самости (Self):
   - 8 качеств: спокойствие, ясность, любопытство, сострадание,
     уверенность, креативность, мужество, связанность
   - Самость может исцелять части

4. Процесс работы:
   - Найти часть
   - Сфокусироваться на ней
   - Узнать о её роли
   - Развить отношения с ней

Помогай пользователю замечать активированные части.
Поощряй любопытство к каждой части, а не борьбу с ней.

Отвечай кратко (2-3 предложения), с состраданием и любопытством.
Это только для образовательной демонстрации."""

TRE_PROMPT = """Ты - специалист по TRE (Упражнениям для высвобождения травмы).
Сосредоточься на:

1. Телесная осознанность:
   - Сканирование тела
   - Замечание напряжения и зажимов
   - Отслеживание ощущений

2. Понимание нейрогенного тремора:
   - Естественный механизм разрядки стресса
   - Тремор как исцеление
   - Безопасность процесса

3. Связь тела и эмоций:
   - Где в теле живут эмоции
   - Паттерны напряжения
   - Соматические ресурсы

4. Техники заземления:
   - 5-4-3-2-1 (сенсорная техника)
   - Дыхательные практики
   - Ориентация в пространстве

Направляй внимание на:
- Дыхание и его паттерны
- Мышечное напряжение
- Физические ощущения, связанные с эмоциями

Замечание: Реальные упражнения TRE требуют профессионального сопровождения.
Отвечай кратко (2-3 предложения), с фокусом на теле.
Это только для образовательной демонстрации."""

MEMORY_PROMPT = """Ты - агент памяти, который извлекает ключевые терапевтические инсайты.
Проанализируй разговор и определи:

- Паттерны мышления или поведения
- Основные проблемы или триггеры  
- Терапевтический прогресс или прорывы
- Важный личный контекст
- Ресурсы и сильные стороны

Ответь ТОЛЬКО в формате JSON:
{{
    "insights": ["инсайт1", "инсайт2"],
    "patterns": ["паттерн1"],
    "triggers": ["триггер1"],
    "resources": ["ресурс1"],
    "keywords": ["ключевое_слово1", "ключевое_слово2"]
}}"""

# agents/base.py
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

# agents/specialists.py
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatLiteLLM
from agents.prompts import (
    ROUTER_PROMPT, DBT_PROMPT, IFS_PROMPT, 
    TRE_PROMPT, MEMORY_PROMPT
)
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

# core/graph.py
from langgraph.graph import StateGraph, END
from agents.specialists import (
    RouterAgent, DBTAgent, IFSAgent, TREAgent, MemoryAgent,
    TherapyState
)
from langchain.schema import HumanMessage, AIMessage
from typing import Dict

class TherapyGraph:
    """Граф обработки сообщений через агентов"""
    
    def __init__(self):
        # Инициализация агентов
        self.router = RouterAgent()
        self.dbt_agent = DBTAgent()
        self.ifs_agent = IFSAgent()
        self.tre_agent = TREAgent()
        self.memory_agent = MemoryAgent()
        
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
    
    def process_message(self, user_message: str, messages: List[BaseMessage] = None) -> Dict:
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

# core/storage.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json

class MemoryStorage:
    """SQLite хранилище для терапевтических сессий"""
    
    def __init__(self, db_path: str = "therapy_sessions.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация таблиц базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица сессий
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица сообщений
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                role TEXT,
                content TEXT,
                approach TEXT,
                confidence REAL,
                reasoning TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        
        # Таблица инсайтов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                insight TEXT,
                type TEXT,  -- 'insight', 'pattern', 'trigger', 'resource'
                approach TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_session(self, user_id: str = "default") -> int:
        """Создать новую сессию"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (user_id) VALUES (?)", (user_id,))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def save_interaction(self, session_id: int, state: Dict):
        """Сохранить полное взаимодействие"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Сохраняем сообщение пользователя
        cursor.execute(
            """INSERT INTO messages 
            (session_id, role, content, approach, confidence, reasoning) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, "user", state["user_message"], None, None, None)
        )
        
        # Сохраняем ответ специалиста
        cursor.execute(
            """INSERT INTO messages 
            (session_id, role, content, approach, confidence, reasoning) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, "assistant", state["specialist_response"],
             state["current_approach"], state["confidence"], state["reasoning"])
        )
        
        # Сохраняем инсайты
        insights = state.get("insights", {})
        
        for insight in insights.get("insights", []):
            cursor.execute(
                """INSERT INTO insights 
                (session_id, insight, type, approach) 
                VALUES (?, ?, ?, ?)""",
                (session_id, insight, "insight", state["current_approach"])
            )
        
        for pattern in insights.get("patterns", []):
            cursor.execute(
                """INSERT INTO insights 
                (session_id, insight, type, approach) 
                VALUES (?, ?, ?, ?)""",
                (session_id, pattern, "pattern", state["current_approach"])
            )
        
        for trigger in insights.get("triggers", []):
            cursor.execute(
                """INSERT INTO insights 
                (session_id, insight, type, approach) 
                VALUES (?, ?, ?, ?)""",
                (session_id, trigger, "trigger", state["current_approach"])
            )
        
        conn.commit()
        conn.close()
    
    def get_session_history(self, session_id: int) -> List[Dict]:
        """Получить историю сессии"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT role, content, approach, confidence, reasoning, created_at
            FROM messages
            WHERE session_id = ?
            ORDER BY created_at
        """, (session_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "role": row[0],
                "content": row[1],
                "approach": row[2],
                "confidence": row[3],
                "reasoning": row[4],
                "created_at": row[5]
            })
        
        conn.close()
        return messages
    
    def get_session_insights(self, session_id: int) -> List[Dict]:
        """Получить инсайты сессии"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT insight, type, approach, created_at
            FROM insights
            WHERE session_id = ?
            ORDER BY created_at DESC
        """, (session_id,))
        
        insights = []
        for row in cursor.fetchall():
            insights.append({
                "insight": row[0],
                "type": row[1],
                "approach": row[2],
                "created_at": row[3]
            })
        
        conn.close()
        return insights

# core/orchestrator.py
from core.graph import TherapyGraph
from core.storage import MemoryStorage
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from typing import List, Dict, Optional

class TherapyOrchestrator:
    """Главный оркестратор системы"""
    
    def __init__(self, use_memory: bool = True):
        self.graph = TherapyGraph()
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

# main.py - CLI интерфейс
from core.orchestrator import TherapyOrchestrator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

def main():
    console.print("\n[bold cyan]🧠 Мультиагентная Терапевтическая Система[/bold cyan]")
    console.print("[yellow]" + "="*60 + "[/yellow]")
    console.print("[red]⚠️  Это образовательная демонстрация, не для реального использования[/red]")
    console.print("[dim]Команды: 'выход' - завершить, 'память' - показать инсайты[/dim]\n")
    
    orchestrator = TherapyOrchestrator(use_memory=True)
    session_id = orchestrator.start_session()
    
    console.print(f"[green]✓ Сессия начата (ID: {session_id})[/green]\n")
    
    while True:
        user_input = console.input("[bold blue]Вы:[/bold blue] ").strip()
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            console.print("\n[yellow]👋 Сессия завершена. Берегите себя![/yellow]")
            break
        
        if user_input.lower() in ['память', 'memory']:
            insights = orchestrator.get_session_insights()
            if insights:
                table = Table(title="📚 Инсайты Сессии")
                table.add_column("Тип", style="cyan")
                table.add_column("Инсайт", style="white")
                table.add_column("Подход", style="green")
                
                for ins in insights[:5]:
                    table.add_row(
                        ins['type'].upper(),
                        ins['insight'],
                        ins['approach']
                    )
                
                console.print(table)
            else:
                console.print("[dim]Пока нет инсайтов[/dim]")
            continue
        
        # Обработка сообщения
        with console.status("[yellow]Обработка...[/yellow]"):
            result = orchestrator.process_message(user_input)
        
        # Показываем метаинформацию
        approach_colors = {
            "DBT": "blue",
            "IFS": "magenta",
            "TRE": "green"
        }
        color = approach_colors.get(result['approach'], 'white')
        
        panel = Panel(
            result['response'],
            title=f"[{color}]{result['approach']}[/{color}] Специалист",
            subtitle=f"[dim]{result['reasoning']} (уверенность: {result['confidence']:.0%})[/dim]"
        )
        console.print(panel)
        
        # Показываем инсайты если есть
        if result.get('insights') and result['insights'].get('insights'):
            rprint(f"[dim]💡 Инсайты: {', '.join(result['insights']['insights'])}[/dim]")

if __name__ == "__main__":
    main()

# app.py - Streamlit интерфейс
import streamlit as st
from core.orchestrator import TherapyOrchestrator
import time

st.set_page_config(
    page_title="Терапевтическая Система",
    page_icon="🧠",
    layout="wide"
)

# Инициализация состояния сессии
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = TherapyOrchestrator(use_memory=True)
    st.session_state.session_id = st.session_state.orchestrator.start_session()
    st.session_state.messages = []

# Заголовок
st.title("🧠 Мультиагентная Терапевтическая Система")
st.warning("⚠️ Образовательная демонстрация - не для реального терапевтического использования")

# Описание подходов
with st.expander("ℹ️ О терапевтических подходах"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### DBT (Диалектическая поведенческая терапия)
        - Эмоциональная регуляция
        - Толерантность к дистрессу
        - Межличностная эффективность
        - Осознанность
        """)
    
    with col2:
        st.markdown("""
        ### IFS (Внутренние семейные системы)
        - Работа с внутренними частями
        - Самолидерство
        - Исцеление травм
        - Внутренняя гармония
        """)
    
    with col3:
        st.markdown("""
        ### TRE (Высвобождение травмы)
        - Телесная осознанность
        - Работа с напряжением
        - Соматические симптомы
        - Нейрогенный тремор
        """)

# Основной интерфейс
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Беседа")
    
    # Контейнер для сообщений
    messages_container = st.container(height=400)
    
    with messages_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg.get("metadata"):
                    st.caption(
                        f"🔍 {msg['metadata']['approach']} "
                        f"({msg['metadata']['confidence']:.0%}) - "
                        f"{msg['metadata']['reasoning']}"
                    )
    
    # Ввод сообщения
    if prompt := st.chat_input("Поделитесь своими мыслями..."):
        # Добавляем сообщение пользователя
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Показываем сообщение пользователя
        with messages_container:
            with st.chat_message("user"):
                st.write(prompt)
        
        # Обрабатываем через агентов
        with st.spinner("Анализ и выбор подхода..."):
            result = st.session_state.orchestrator.process_message(prompt)
        
        # Добавляем ответ
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "metadata": {
                "approach": result["approach"],
                "confidence": result["confidence"],
                "reasoning": result["reasoning"]
            }
        })
        
        # Показываем ответ
        with messages_container:
            with st.chat_message("assistant"):
                st.write(result["response"])
                st.caption(
                    f"🔍 {result['approach']} "
                    f"({result['confidence']:.0%}) - "
                    f"{result['reasoning']}"
                )
        
        # Перезагружаем для обновления
        st.rerun()

with col2:
    st.subheader("📊 Статистика сессии")
    
    # Счетчики подходов
    approaches_count = {"DBT": 0, "IFS": 0, "TRE": 0}
    for msg in st.session_state.messages:
        if msg.get("metadata") and msg["metadata"].get("approach"):
            approaches_count[msg["metadata"]["approach"]] += 1
    
    # Метрики
    st.metric("Сообщений", len(st.session_state.messages))
    
    for approach, count in approaches_count.items():
        emoji = {"DBT": "🧘", "IFS": "👥", "TRE": "💪"}
        st.metric(f"{emoji.get(approach, '')} {approach}", count)
    
    st.divider()
    
    # Инсайты
    if st.button("🔄 Обновить инсайты"):
        insights = st.session_state.orchestrator.get_session_insights()
        
        if insights:
            st.subheader("💡 Инсайты сессии")
            
            for insight in insights[:5]:
                insight_type = {
                    "insight": "💡",
                    "pattern": "🔄",
                    "trigger": "⚡",
                    "resource": "💪"
                }.get(insight['type'], "📝")
                
                with st.expander(
                    f"{insight_type} {insight['type'].title()} - {insight['approach']}"
                ):
                    st.write(insight['insight'])
        else:
            st.info("Пока нет инсайтов")

# Кнопка экспорта истории
if st.sidebar.button("📥 Экспортировать историю"):
    history = st.session_state.orchestrator.get_session_history()
    st.sidebar.download_button(
        "Скачать JSON",
        data=json.dumps(history, ensure_ascii=False, indent=2),
        file_name=f"session_{st.session_state.session_id}.json",
        mime="application/json"
    )

# .env.example
"""
# Примеры настройки для разных провайдеров

# OpenAI
MODEL=gpt-4
OPENAI_API_KEY=your-key-here

# Anthropic
# MODEL=claude-3-haiku-20240307
# ANTHROPIC_API_KEY=your-key-here

# Google
# MODEL=gemini-pro
# GOOGLE_API_KEY=your-key-here

# YandexGPT
# MODEL=yandexgpt/latest
# YANDEX_API_KEY=your-key-here

# Локальная модель через Ollama
# MODEL=ollama/llama2
# Не требует API ключа

# Azure OpenAI
# MODEL=azure/gpt-4
# AZURE_API_KEY=your-key-here
# AZURE_API_BASE=https://your-resource.openai.azure.com
# AZURE_API_VERSION=2023-05-15
"""