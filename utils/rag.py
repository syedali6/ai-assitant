"""
utils/rag.py — RAG chain construction and querying.

Builds a ConversationalRetrievalChain that:
    • Retrieves relevant document chunks via FAISS similarity search
    • Passes chunks as context to the configured LLM
    • Maintains a sliding-window conversation memory
    • Returns the answer and source document references
"""

from typing import Dict, Any, List
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.retrievers import BaseRetriever

import config


# ─────────────────────────────────────────────
# LLM Factory
# ─────────────────────────────────────────────

def get_llm():
    """Return the configured LLM instance.

    Returns:
        A LangChain chat model (ChatOpenAI or ChatGoogleGenerativeAI).

    Raises:
        ValueError: If provider is unsupported or API key is missing.
    """
    provider = config.LLM_PROVIDER.lower()

    if provider == "openai":
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Please add it to your .env file or enter it in the sidebar."
            )
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            model=config.OPENAI_MODEL,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS,
        )

    elif provider == "gemini":
        if not config.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not set. "
                "Please add it to your .env file or enter it in the sidebar."
            )
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            google_api_key=config.GOOGLE_API_KEY,
            model=config.GEMINI_MODEL,
            temperature=config.LLM_TEMPERATURE,
            max_output_tokens=config.LLM_MAX_TOKENS,
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: '{config.LLM_PROVIDER}'. "
            "Choose 'openai' or 'gemini'."
        )


# ─────────────────────────────────────────────
# Memory Factory
# ─────────────────────────────────────────────

def get_memory() -> ConversationBufferWindowMemory:
    """Create a sliding-window conversation memory.

    Returns:
        ConversationBufferWindowMemory keeping the last MEMORY_WINDOW turns.
    """
    return ConversationBufferWindowMemory(
        k=config.MEMORY_WINDOW,
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )


# ─────────────────────────────────────────────
# Chain Builder
# ─────────────────────────────────────────────

def build_qa_chain(retriever: BaseRetriever, llm=None, memory=None) -> ConversationalRetrievalChain:
    """Build a ConversationalRetrievalChain with memory.

    Args:
        retriever: LangChain retriever from the FAISS vector store.
        llm:       Optional pre-built LLM (calls get_llm() if None).
        memory:    Optional pre-built memory (calls get_memory() if None).

    Returns:
        A ready-to-query ConversationalRetrievalChain.
    """
    llm    = llm    or get_llm()
    memory = memory or get_memory()

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
    )
    return chain


# ─────────────────────────────────────────────
# Query Helper
# ─────────────────────────────────────────────

def query(chain: ConversationalRetrievalChain, question: str) -> Dict[str, Any]:
    """Run a question through the RAG chain.

    Args:
        chain:    Built ConversationalRetrievalChain.
        question: User's natural-language question.

    Returns:
        Dict with keys:
            • "answer"  (str)        — LLM-generated answer
            • "sources" (List[dict]) — list of {source, chunk_index} dicts
    """
    result = chain.invoke({"question": question})

    answer = result.get("answer", "")
    source_docs = result.get("source_documents", [])

    # Deduplicate and format sources
    seen = set()
    sources: List[dict] = []
    for doc in source_docs:
        meta = doc.metadata
        key  = (meta.get("source", "Unknown"), meta.get("chunk_index", 0))
        if key not in seen:
            seen.add(key)
            sources.append({
                "source":      meta.get("source", "Unknown"),
                "chunk_index": meta.get("chunk_index", 0),
                "total_chunks": meta.get("total_chunks", "?"),
                "snippet":     doc.page_content[:200].strip(),
            })

    return {"answer": answer, "sources": sources}
