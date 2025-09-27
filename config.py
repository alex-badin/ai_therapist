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