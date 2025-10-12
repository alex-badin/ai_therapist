import json

import streamlit as st

import agents.prompts as prompt_defaults
from core.orchestrator import TherapyOrchestrator
from services.prompt_store import PROMPT_KEYS, PromptStore


PROMPT_LABELS = {
    "router": "Маршрутизатор",
    "dbt": "DBT",
    "ifs": "IFS",
    "tre": "TRE",
    "memory": "Память",
}

DEFAULT_PROMPTS = {
    "router": prompt_defaults.ROUTER_PROMPT,
    "dbt": prompt_defaults.DBT_PROMPT,
    "ifs": prompt_defaults.IFS_PROMPT,
    "tre": prompt_defaults.TRE_PROMPT,
    "memory": prompt_defaults.MEMORY_PROMPT,
}

st.set_page_config(
    page_title="Терапевтическая Система",
    page_icon="🧠",
    layout="wide"
)

# Инициализация состояния сессии
if 'prompt_store' not in st.session_state:
    st.session_state.prompt_store = PromptStore()

if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = TherapyOrchestrator(
        use_memory=True,
        prompt_store=st.session_state.prompt_store,
    )
    st.session_state.session_id = st.session_state.orchestrator.start_session()
    st.session_state.messages = []

# Заголовок
st.title("🧠 Мультиагентная Терапевтическая Система")
st.warning("⚠️ Образовательная демонстрация - не для реального терапевтического использования")

# Боковая панель: управление промптами и экспорт
prompt_store = st.session_state.prompt_store

with st.sidebar:
    st.subheader("⚙️ Настройки")
    st.caption(f"Google Sheets: {prompt_store.status()}")

    if prompt_store.enabled:
        overrides = prompt_store.load_all()
        current_prompts = dict(DEFAULT_PROMPTS)
        for key, record in overrides.items():
            if record.prompt:
                current_prompts[key] = record.prompt

        with st.form("prompt_editor"):
            st.markdown("**🛠️ Редактор промптов**")
            edited_prompts = {}
            for key in PROMPT_KEYS:
                label = PROMPT_LABELS.get(key, key.upper())
                edited_prompts[key] = st.text_area(
                    label,
                    current_prompts.get(key, DEFAULT_PROMPTS[key]),
                    height=160,
                )

            default_name = st.session_state.get("prompt_editor_name", "")
            editor_name = st.text_input("Имя редактора (необязательно)", value=default_name)
            submitted = st.form_submit_button("💾 Сохранить промпты")

        if submitted:
            st.session_state["prompt_editor_name"] = editor_name
            normalized_name = editor_name.strip() or None
            changes_made = False
            errors = []

            for key, new_value in edited_prompts.items():
                existing_record = overrides.get(key)
                existing_value = (
                    existing_record.prompt if existing_record and existing_record.prompt else DEFAULT_PROMPTS[key]
                )
                if new_value != existing_value:
                    success = prompt_store.update_prompt(key, new_value, updated_by=normalized_name)
                    if not success:
                        errors.append(key)
                        break
                    changes_made = True

            if errors:
                readable = ", ".join(PROMPT_LABELS.get(key, key) for key in errors)
                st.error(f"Не удалось обновить промпт(ы): {readable}")
            elif changes_made:
                st.session_state.orchestrator.refresh_prompts()
                st.success("Промпты обновлены")
                st.rerun()
            else:
                st.info("Изменений не обнаружено")
    else:
        st.info("Редактирование промптов отключено. Проверьте настройки Google Sheets в secrets.toml.")

    st.divider()

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
