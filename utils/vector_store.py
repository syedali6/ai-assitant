"""
utils/vector_store.py — FAISS vector database management.

Provides helpers to:
    • build a fresh FAISS index from documents
    • add new documents to an existing index (multi-upload support)
    • create a LangChain retriever from the index
"""

from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
import config


def build_vector_store(documents: List[Document], embeddings) -> FAISS:
    """Create a new FAISS vector store from a list of LangChain Documents.

    Args:
        documents:  List of Document objects (chunked).
        embeddings: LangChain Embeddings instance.

    Returns:
        A populated FAISS vector store.
    """
    if not documents:
        raise ValueError("Cannot build a vector store from an empty document list.")
    return FAISS.from_documents(documents, embeddings)


def add_documents(
    vector_store: FAISS,
    documents: List[Document],
    embeddings,
) -> FAISS:
    """Add more documents to an existing FAISS index (incremental upload).

    Args:
        vector_store: Existing FAISS vector store to extend.
        documents:    New Document objects to add.
        embeddings:   LangChain Embeddings instance.

    Returns:
        Updated FAISS vector store.
    """
    if not documents:
        return vector_store
    vector_store.add_documents(documents)
    return vector_store


def get_retriever(vector_store: FAISS, k: Optional[int] = None):
    """Create a LangChain retriever from a FAISS vector store.

    Args:
        vector_store: Populated FAISS vector store.
        k:            Number of top results to retrieve. Defaults to config.RETRIEVER_K.

    Returns:
        LangChain VectorStoreRetriever.
    """
    k = k or config.RETRIEVER_K
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


def save_index(vector_store: FAISS, path: Optional[str] = None) -> None:
    """Persist FAISS index to disk.

    Args:
        vector_store: FAISS vector store to save.
        path:         Directory path. Defaults to config.FAISS_INDEX_PATH.
    """
    path = path or config.FAISS_INDEX_PATH
    vector_store.save_local(path)


def load_index(embeddings, path: Optional[str] = None) -> FAISS:
    """Load a persisted FAISS index from disk.

    Args:
        embeddings: LangChain Embeddings instance (must match the saved index).
        path:       Directory path. Defaults to config.FAISS_INDEX_PATH.

    Returns:
        Loaded FAISS vector store.
    """
    path = path or config.FAISS_INDEX_PATH
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
