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