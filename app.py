import streamlit as st
from core.orchestrator import TherapyOrchestrator
import time
import json

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