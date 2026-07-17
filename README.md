# 🔬 AI Research Assistant

> **Retrieval-Augmented Generation (RAG)** powered by LangChain, FAISS, and GPT-4o / Gemini 1.5 Pro

A production-grade intelligent research assistant that answers questions by searching your uploaded documents and generating context-aware responses via Large Language Models.

---

## ✨ Features

| Feature | Details |
|---|---|
| 📄 Document Support | PDF, DOCX, TXT |
| 🔍 Semantic Search | FAISS vector similarity search |
| 🧠 LLM Backends | OpenAI GPT-4o **or** Google Gemini 1.5 Pro |
| 🗂️ Embeddings | HuggingFace `all-MiniLM-L6-v2` (free) or OpenAI |
| 💬 Conversation Memory | Sliding-window buffer (last 5 turns) |
| 📎 Source Attribution | Every answer cites originating document + chunk |
| 📚 Multi-Document | Upload multiple files in one session |
| ⚙️ Configurable | Chunk size, overlap, top-k, temperature via UI |

---

## 🏗️ Architecture

```
User Uploads Files
      │
      ▼
Text Extraction         ← utils/loader.py    (PyPDF2, python-docx)
      │
      ▼
Text Chunking           ← utils/chunking.py  (RecursiveCharacterTextSplitter)
      │
      ▼
Embedding Model         ← utils/embeddings.py (HuggingFace / OpenAI)
      │
      ▼
FAISS Vector DB         ← utils/vector_store.py
      │
      ▼
Similarity Search (top-k)
      │
      ▼
ConversationalRetrievalChain ← utils/rag.py  (LangChain + Memory)
      │
      ▼
LLM (GPT-4o / Gemini)
      │
      ▼
Answer + Source References
      │
      ▼
Streamlit Chat UI       ← app.py
```

---

## 📁 Project Structure

```
AI-Research-Assistant/
│
├── app.py                  # Streamlit UI (entry point)
├── config.py               # Centralised configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md
│
├── data/                   # Sample / test documents
│
└── utils/
    ├── __init__.py
    ├── loader.py           # PDF / DOCX / TXT extraction
    ├── chunking.py         # Text splitting → LangChain Documents
    ├── embeddings.py       # Embeddings factory
    ├── vector_store.py     # FAISS index management
    └── rag.py              # LLM + chain + query logic
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone <your-repo-url>
cd ai-research-assistant

pip install -r requirements.txt
```

### 2. Configure API keys

```bash
# Copy the template
cp .env.example .env

# Edit .env and add your key:
GOOGLE_API_KEY=AIza...          # for Gemini (default)
# OR
OPENAI_API_KEY=sk-...           # for GPT-4o
```

> **Note**: Embeddings use HuggingFace by default — **no API key needed** for embeddings.

### 3. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🔧 Configuration

All settings live in `config.py` and can be overridden via `.env` or the **Advanced Settings** panel in the sidebar:

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `gemini` | `"gemini"` or `"openai"` |
| `GEMINI_MODEL` | `gemini-3.5-flash` | Gemini model name |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model name |
| `EMBEDDING_PROVIDER` | `huggingface` | `"huggingface"` or `"openai"` |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVER_K` | `5` | Top-k chunks retrieved |
| `LLM_TEMPERATURE` | `0.3` | LLM creativity (0–1) |
| `MEMORY_WINDOW` | `5` | Conversation turns to keep |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — Chat UI
- **LangChain** — RAG chain, memory, splitters
- **FAISS** — Vector similarity search
- **HuggingFace Sentence Transformers** — Free embeddings
- **PyPDF2** — PDF extraction
- **python-docx** — DOCX extraction
- **OpenAI / Google Generative AI** — LLM backends

---

## 💡 Resume Points

- Developed a **Retrieval-Augmented Generation (RAG)** application using LangChain and OpenAI/Gemini APIs
- Implemented **semantic search** with FAISS vector database for efficient document retrieval
- Built a **document processing pipeline** supporting PDF, DOCX, and TXT files
- Integrated LLMs to generate **context-aware answers** based on retrieved information
- Designed a **Streamlit-based conversational interface** with source attribution
- Optimised retrieval accuracy using **document chunking and embedding** techniques
- Implemented **conversation memory** with sliding-window buffer for multi-turn Q&A


