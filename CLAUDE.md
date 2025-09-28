# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-agent AI therapy system built with LangGraph that demonstrates different therapeutic approaches. It's an educational project showing how specialized agents can route conversations to appropriate therapeutic modalities.

⚠️ **Educational demonstration only - not for real therapeutic use**

## Architecture

The system uses a **LangGraph-based multi-agent architecture** with the following flow:

```
User Input → Router Agent → [DBT/IFS/TRE Specialist] → Memory Agent → Response + Insights
```

### Core Components

- **Router Agent** (`agents/specialists.py:RouterAgent`) - Analyzes user input and selects appropriate therapeutic approach
- **Specialist Agents** - Three therapeutic modalities:
  - **DBT Agent** - Dialectical Behavioral Therapy (emotional regulation, distress tolerance)
  - **IFS Agent** - Internal Family Systems (working with internal parts)
  - **TRE Agent** - Trauma Release Exercises (body awareness, somatic work)
- **Memory Agent** - Extracts insights from conversations and stores them
- **Orchestrator** (`core/orchestrator.py`) - Main coordinator that manages sessions and database storage
- **LangGraph Workflow** (`core/graph.py`) - Defines the agent routing and execution flow

### Key Files

- `main.py` - CLI interface with Rich formatting
- `app.py` - Streamlit web interface
- `core/orchestrator.py` - Session management and agent coordination
- `core/graph.py` - LangGraph workflow definition
- `core/storage.py` - SQLite session storage
- `agents/specialists.py` - All agent implementations
- `agents/prompts.py` - Therapeutic prompts for each approach
- `config.py` - LiteLLM configuration for multiple AI providers

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (copy and edit with your API keys)
cp .env.example .env
```

### Running the Application
```bash
# CLI interface
python main.py

# Web interface (Streamlit)
streamlit run app.py
```

### Configuration

The system uses **LiteLLM** for model access, supporting multiple providers. Configure in `.env`:

```env
# Examples:
MODEL=gpt-4                          # OpenAI
MODEL=claude-3-haiku-20240307        # Anthropic
MODEL=gemini-pro                     # Google
MODEL=ollama/llama2                  # Local Ollama
MODEL=yandexgpt/latest               # YandexGPT
```

## Database Storage

- Sessions stored in SQLite (`therapy_sessions.db`)
- Tracks conversation history, insights, and metadata
- Memory agent extracts patterns and therapeutic insights automatically

## Agent Routing Logic

The router agent analyzes user input for:
- **Emotional regulation keywords** → DBT
- **Internal conflict/parts language** → IFS
- **Physical symptoms/trauma** → TRE

Each specialist uses tailored prompts from `agents/prompts.py` and returns responses with confidence scores and reasoning.