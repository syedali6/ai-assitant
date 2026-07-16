"""
app.py — AI Research Assistant: Streamlit Chat UI
"""

import os
import time
import streamlit as st

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inline CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  /* ── Global reset ── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ── Background ── */
  .stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2e 40%, #0f1f35 100%);
    min-height: 100vh;
  }

  /* ── Hide default streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1524 0%, #111d30 100%) !important;
    border-right: 1px solid rgba(99,179,237,0.15) !important;
  }
  [data-testid="stSidebar"] * { color: #cbd5e1 !important; }

  /* ── Custom header ── */
  .app-header {
    background: linear-gradient(135deg, rgba(13,25,50,0.9), rgba(15,31,53,0.95));
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
  }
  .app-title {
    font-size: 2rem;
    font-weight: 700;
    background: white;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 4px 0;
  }
  .app-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin: 0;
    font-weight: 400;
  }

  /* ── Status badge ── */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .status-ready   { background: rgba(72,187,120,0.15); color: #68d391; border: 1px solid rgba(72,187,120,0.3); }
  .status-waiting { background: rgba(246,173,85,0.15);  color: #f6ad55; border: 1px solid rgba(246,173,85,0.3); }

  /* ── Chat container ── */
  .chat-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: 60vh;
    overflow-y: auto;
    padding: 8px 4px;
    scrollbar-width: thin;
    scrollbar-color: rgba(99,179,237,0.3) transparent;
  }

  /* ── Message bubbles ── */
  .msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 4px;
  }
  .msg-assistant {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 4px;
  }
  .bubble-user {
    background: linear-gradient(135deg, #2d6a9f, #3b82c4);
    color: #f0f9ff;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(45,106,159,0.3);
    word-wrap: break-word;
  }
  .bubble-assistant {
    background: rgba(17,29,48,0.85);
    border: 1px solid rgba(99,179,237,0.2);
    color: #e2e8f0;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 78%;
    font-size: 0.92rem;
    line-height: 1.7;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    word-wrap: break-word;
    backdrop-filter: blur(8px);
  }
  .avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
  }
  .avatar-user      { background: linear-gradient(135deg,#2d6a9f,#9f7aea); margin-left: 8px; }
  .avatar-assistant { background: linear-gradient(135deg,#1a2d4e,#0d4f7d); margin-right: 8px; border: 1px solid rgba(99,179,237,0.3); }

  /* ── Source cards ── */
  .sources-header {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 10px 0 6px 0;
  }
  .source-card {
    background: rgba(13,25,50,0.7);
    border: 1px solid rgba(99,179,237,0.15);
    border-left: 3px solid #63b3ed;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    font-size: 0.8rem;
    color: #94a3b8;
    backdrop-filter: blur(4px);
  }
  .source-filename {
    color: #63b3ed;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
  }
  .source-snippet {
    color: #64748b;
    font-size: 0.76rem;
    margin-top: 4px;
    font-style: italic;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* ── Upload area ── */
  .upload-section {
    background: rgba(13,25,50,0.6);
    border: 1px dashed rgba(99,179,237,0.3);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    text-align: center;
    transition: border-color 0.3s ease;
  }

  /* ── Doc pill ── */
  .doc-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 0.75rem;
    color: #63b3ed;
    margin: 3px;
    font-family: 'JetBrains Mono', monospace;
  }

  /* ── Stats bar ── */
  .stats-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 12px 0;
  }
  .stat-card {
    background: rgba(13,25,50,0.7);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 10px;
    padding: 10px 16px;
    flex: 1;
    min-width: 90px;
    text-align: center;
  }
  .stat-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #63b3ed;
    display: block;
    line-height: 1;
  }
  .stat-label {
    font-size: 0.65rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
  }

  /* ── Input area ── */
  .stTextInput > div > div > input,
  .stChatInput > div > div > textarea {
    background: rgba(13,25,50,0.8) !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
  }
  .stChatInput > div > div > textarea:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.15) !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #1a4a7a, #2563a0) !important;
    border: 1px solid rgba(99,179,237,0.3) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #2563a0, #3b82c4) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(99,179,237,0.2) !important;
  }

  /* ── Spinner ── */
  .thinking-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: rgba(13,25,50,0.6);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 12px;
    color: #94a3b8;
    font-size: 0.85rem;
  }
  .dot-pulse {
    display: flex;
    gap: 4px;
    align-items: center;
  }
  .dot-pulse span {
    width: 7px; height: 7px;
    background: #63b3ed;
    border-radius: 50%;
    display: inline-block;
    animation: dotPulse 1.4s infinite ease-in-out;
  }
  .dot-pulse span:nth-child(2) { animation-delay: 0.2s; }
  .dot-pulse span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes dotPulse {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
    40%            { transform: scale(1.0); opacity: 1.0; }
  }

  /* ── Divider ── */
  hr { border-color: rgba(99,179,237,0.1) !important; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.25); border-radius: 3px; }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    background: rgba(13,25,50,0.5) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Imports (after page config) ──────────────────────────────────────────────
from utils.loader      import load_document
from utils.chunking    import chunk_text
from utils.embeddings  import get_embeddings
from utils.vector_store import build_vector_store, add_documents, get_retriever
from utils.rag         import build_qa_chain, get_memory, query
import config


# ─── Session State Initialisation ─────────────────────────────────────────────
def init_session():
    defaults = {
        "messages":       [],      # [{role, content, sources}]
        "vector_store":   None,
        "qa_chain":       None,
        "memory":         None,
        "embeddings":     None,
        "uploaded_docs":  [],      # list of filenames already processed
        "doc_stats":      {},      # filename → metadata
        "total_chunks":   0,
        "ready":          False,
        "api_key_set":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─── Helper: render a single chat message ─────────────────────────────────────
def render_message(role: str, content: str, sources: list = None):
    if role == "user":
        st.markdown(f"""
        <div class="msg-user">
          <div class="bubble-user">{content}</div>
          <div class="avatar avatar-user">👤</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-assistant">
          <div class="avatar avatar-assistant">🔬</div>
          <div class="bubble-assistant">{content}</div>
        </div>
        """, unsafe_allow_html=True)

        if sources:
            st.markdown('<div class="sources-header">📎 Source References</div>', unsafe_allow_html=True)
            for s in sources:
                chunk_label = f"Chunk {s['chunk_index']+1} / {s['total_chunks']}"
                st.markdown(f"""
                <div class="source-card">
                  <span class="source-filename">📄 {s['source']}</span>
                  &nbsp;&nbsp;<span style="color:#475569;font-size:0.72rem">{chunk_label}</span>
                  <div class="source-snippet">"{s['snippet']}..."</div>
                </div>
                """, unsafe_allow_html=True)


# ─── Helper: process uploaded file ────────────────────────────────────────────
def process_file(uploaded_file) -> bool:
    """Extract, chunk, embed, and add a file to the vector store.

    Returns True on success, False on failure.
    """
    if uploaded_file.name in st.session_state.uploaded_docs:
        st.sidebar.warning(f"'{uploaded_file.name}' is already loaded.", icon="⚠️")
        return False

    try:
        with st.sidebar.status(f"Processing **{uploaded_file.name}**...", expanded=True) as status:
            # 1. Extract text
            status.update(label="📄 Extracting text...")
            text, filename, metadata = load_document(uploaded_file)

            if not text.strip():
                st.sidebar.error(f"No text could be extracted from '{filename}'.")
                return False

            # 2. Chunk
            status.update(label="✂️ Chunking text...")
            docs = chunk_text(text, filename, extra_metadata=metadata)

            # 3. Embed + store
            if st.session_state.embeddings is None:
                status.update(label="⚡ Loading embedding model...")
                st.session_state.embeddings = get_embeddings()

            status.update(label="🗄️ Building vector index...")
            if st.session_state.vector_store is None:
                st.session_state.vector_store = build_vector_store(docs, st.session_state.embeddings)
            else:
                st.session_state.vector_store = add_documents(
                    st.session_state.vector_store, docs, st.session_state.embeddings
                )

            # 4. Rebuild chain with updated retriever
            status.update(label="🔗 Updating retrieval chain...")
            retriever = get_retriever(st.session_state.vector_store)

            if st.session_state.memory is None:
                st.session_state.memory = get_memory()

            st.session_state.qa_chain = build_qa_chain(
                retriever=retriever,
                memory=st.session_state.memory,
            )

            # 5. Record
            st.session_state.uploaded_docs.append(filename)
            st.session_state.doc_stats[filename] = metadata
            st.session_state.total_chunks += len(docs)
            st.session_state.ready = True

            status.update(label=f"✅ '{filename}' ready! ({len(docs)} chunks)", state="complete")
        return True

    except ValueError as e:
        st.sidebar.error(str(e))
        return False
    except Exception as e:
        st.sidebar.error(f"Error processing file: {e}")
        return False


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 12px 0 20px 0;">
      <div style="font-size:2.5rem;">🔬</div>
      <div style="font-size:1.1rem; font-weight:700; color:#63b3ed; margin-top:4px;">AI Research Assistant</div>
      <div style="font-size:0.72rem; color:#475569; margin-top:2px;">RAG · LangChain · FAISS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── API Configuration ──
    st.markdown("#### ⚙️ LLM Configuration")

    llm_choice = st.selectbox(
        "LLM Provider",
        ["Gemini (Google)", "OpenAI (GPT-4o)"],
        index=0,
        help="Select your LLM backend.",
    )
    config.LLM_PROVIDER = "gemini" if "Gemini" in llm_choice else "openai"

    if config.LLM_PROVIDER == "gemini":
        key_input = st.text_input(
            "Google API Key",
            type="password",
            value=config.GOOGLE_API_KEY or "",
            placeholder="AIza...",
            help="Get your key at https://aistudio.google.com/",
        )
        if key_input:
            config.GOOGLE_API_KEY = key_input
            os.environ["GOOGLE_API_KEY"] = key_input
            st.session_state.api_key_set = True
        else:
            st.session_state.api_key_set = bool(config.GOOGLE_API_KEY)
    else:
        key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=config.OPENAI_API_KEY or "",
            placeholder="sk-...",
            help="Get your key at https://platform.openai.com/",
        )
        if key_input:
            config.OPENAI_API_KEY = key_input
            os.environ["OPENAI_API_KEY"] = key_input
            st.session_state.api_key_set = True
        else:
            st.session_state.api_key_set = bool(config.OPENAI_API_KEY)

    if st.session_state.api_key_set:
        st.markdown('<span class="status-badge status-ready">● API Key Set</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-waiting">○ API Key Required</span>', unsafe_allow_html=True)

    # st.markdown("---")

    # ── Advanced Settings ──
    # with st.expander("🛠️ Advanced Settings"):
    #     config.CHUNK_SIZE = st.slider("Chunk Size", 300, 2000, config.CHUNK_SIZE, 100)
    #     config.CHUNK_OVERLAP = st.slider("Chunk Overlap", 0, 500, config.CHUNK_OVERLAP, 50)
    #     config.RETRIEVER_K = st.slider("Top-K Chunks", 1, 10, config.RETRIEVER_K)
    #     config.LLM_TEMPERATURE = st.slider("Temperature", 0.0, 1.0, config.LLM_TEMPERATURE, 0.05)
    #     emb_choice = st.selectbox(
    #         "Embedding Model",
    #         ["HuggingFace (free)", "OpenAI"],
    #         index=0 if config.EMBEDDING_PROVIDER == "huggingface" else 1,
    #     )
    #     config.EMBEDDING_PROVIDER = "huggingface" if "HuggingFace" in emb_choice else "openai"

    # st.markdown("---")

    # ── File Upload ──
    st.markdown("#### 📂 Upload Documents")
    st.markdown(
        '<div style="font-size:0.75rem; color:#64748b; margin-bottom:8px;">'
        'Supported: PDF · DOCX · TXT</div>',
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Drop files here",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files and st.session_state.api_key_set:
        for f in uploaded_files:
            process_file(f)
    elif uploaded_files and not st.session_state.api_key_set:
        st.warning("Please enter your API key before uploading documents.", icon="🔑")

    # ── Loaded Documents ──
    if st.session_state.uploaded_docs:
        st.markdown("#### 📚 Loaded Documents")
        for fname in st.session_state.uploaded_docs:
            meta = st.session_state.doc_stats.get(fname, {})
            ftype = meta.get("file_type", "")
            icon = {"PDF": "📕", "DOCX": "📘", "TXT": "📄"}.get(ftype, "📄")
            st.markdown(f'<div class="doc-pill">{icon} {fname}</div>', unsafe_allow_html=True)

        # Stats
        n_docs   = len(st.session_state.uploaded_docs)
        n_chunks = st.session_state.total_chunks
        st.markdown(f"""
        <div class="stats-row" style="margin-top:12px;">
          <div class="stat-card">
            <span class="stat-value">{n_docs}</span>
            <div class="stat-label">Documents</div>
          </div>
          <div class="stat-card">
            <span class="stat-value">{n_chunks}</span>
            <div class="stat-label">Chunks</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🗑️ Clear Session", use_container_width=True):
            for key in ["messages", "vector_store", "qa_chain", "memory", "embeddings",
                        "uploaded_docs", "doc_stats", "total_chunks", "ready", "api_key_set"]:
                del st.session_state[key]
            st.rerun()


# ─── MAIN AREA ───────────────────────────────────────────────────────────────

# Header
ready_badge = (
    '<span class="status-badge status-ready">● Ready</span>'
    if st.session_state.ready else
    '<span class="status-badge status-waiting">○ Upload documents to begin</span>'
)
st.markdown(f"""
<div class="app-header">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
    <div>
      <h1 class="app-title">🔬 AI Research Assistant</h1>
      <p class="app-subtitle">
        Retrieval-Augmented Generation · LangChain · FAISS · GPT-4o / Gemini
      </p>
    </div>
    <div style="padding-top:6px;">{ready_badge}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Welcome message (only when empty)
if not st.session_state.messages:
    st.markdown("""
    <div style="
      background: rgba(13,25,50,0.5);
      border: 1px solid rgba(99,179,237,0.15);
      border-radius: 16px;
      padding: 32px;
      text-align: center;
      margin: 24px 0;
    ">
      <div style="font-size:3rem; margin-bottom:12px;">📖</div>
      <h3 style="color:#63b3ed; font-size:1.2rem; margin:0 0 8px 0;">How to get started</h3>
      <div style="color:#64748b; font-size:0.88rem; line-height:1.8; max-width:500px; margin:0 auto;">
        <b style="color:#94a3b8;">1.</b> Enter your API key in the sidebar<br>
        <b style="color:#94a3b8;">2.</b> Upload your PDF, DOCX, or TXT documents<br>
        <b style="color:#94a3b8;">3.</b> Ask questions in natural language below<br>
        <b style="color:#94a3b8;">4.</b> Get accurate answers with source citations
      </div>
    </div>
    """, unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"], msg.get("sources"))

# Chat input
placeholder = (
    "Ask a question about your documents…"
    if st.session_state.ready
    else "Upload documents via the sidebar to begin…"
)

if prompt := st.chat_input(placeholder, disabled=not st.session_state.ready):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    # Show thinking indicator
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
    <div class="msg-assistant">
      <div class="avatar avatar-assistant">🔬</div>
      <div class="thinking-indicator">
        <div class="dot-pulse">
          <span></span><span></span><span></span>
        </div>
        <span>Searching documents and generating answer…</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Run RAG
    try:
        result   = query(st.session_state.qa_chain, prompt)
        answer   = result["answer"]
        sources  = result["sources"]
    except Exception as e:
        answer  = f"⚠️ An error occurred: {str(e)}"
        sources = []

    thinking_placeholder.empty()

    # Store and render assistant response
    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": sources,
    })
    render_message("assistant", answer, sources)
    st.rerun()
