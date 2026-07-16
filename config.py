"""
config.py — Centralized configuration for the AI Research Assistant.

Set your API keys as environment variables or in a .env file:
    OPENAI_API_KEY=sk-...
    GOOGLE_API_KEY=AIza...
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# LLM Backend — "openai" or "gemini"
# ─────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")   # default: gemini

# OpenAI settings
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL     = os.getenv("OPENAI_MODEL", "gpt-4o")

# Google Gemini settings
GOOGLE_API_KEY   = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL     = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# ─────────────────────────────────────────────
# Embedding Backend — "huggingface" or "openai"
# ─────────────────────────────────────────────
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface")
HUGGINGFACE_MODEL  = os.getenv("HUGGINGFACE_MODEL", "all-MiniLM-L6-v2")

# ─────────────────────────────────────────────
# Text Chunking
# ─────────────────────────────────────────────
CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

# ─────────────────────────────────────────────
# Retrieval
# ─────────────────────────────────────────────
RETRIEVER_K = int(os.getenv("RETRIEVER_K", 5))   # top-k chunks to retrieve

# ─────────────────────────────────────────────
# Conversation Memory
# ─────────────────────────────────────────────
MEMORY_WINDOW = int(os.getenv("MEMORY_WINDOW", 5))  # number of past turns to keep

# ─────────────────────────────────────────────
# LLM Generation
# ─────────────────────────────────────────────
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.3))
LLM_MAX_TOKENS  = int(os.getenv("LLM_MAX_TOKENS", 1024))

# ─────────────────────────────────────────────
# FAISS persistence (optional)
# ─────────────────────────────────────────────
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index")
