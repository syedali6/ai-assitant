"""
utils/chunking.py — Text splitting and LangChain Document creation.

Uses LangChain's RecursiveCharacterTextSplitter to break long documents
into overlapping chunks suitable for embedding and retrieval.
"""

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import config


def chunk_text(text: str, source_name: str, extra_metadata: dict = None) -> List[Document]:
    """Split raw text into overlapping chunks and wrap as LangChain Documents.

    Args:
        text:           Full extracted text of the document.
        source_name:    Filename / label used for source attribution.
        extra_metadata: Optional additional metadata dict to merge in.

    Returns:
        List of LangChain Document objects, each with metadata:
            {source, chunk_index, total_chunks}
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    raw_chunks = splitter.split_text(text)
    total = len(raw_chunks)

    documents = []
    for idx, chunk in enumerate(raw_chunks):
        metadata = {
            "source": source_name,
            "chunk_index": idx,
            "total_chunks": total,
        }
        if extra_metadata:
            metadata.update(extra_metadata)

        documents.append(Document(page_content=chunk, metadata=metadata))

    return documents
