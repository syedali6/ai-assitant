"""
utils/loader.py — Document loading and text extraction.

Supports:
    • PDF  (.pdf)  — PyPDF2
    • DOCX (.docx) — python-docx
    • TXT  (.txt)  — plain read
"""

import io
import PyPDF2
import docx
from typing import Tuple


def load_pdf(file_bytes: bytes, filename: str) -> Tuple[str, int]:
    """Extract text from a PDF file.

    Args:
        file_bytes: Raw bytes of the PDF file.
        filename:   Original filename (used for metadata).

    Returns:
        Tuple of (extracted_text, page_count).
    """
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages), len(reader.pages)


def load_docx(file_bytes: bytes) -> Tuple[str, int]:
    """Extract text from a DOCX file.

    Args:
        file_bytes: Raw bytes of the DOCX file.

    Returns:
        Tuple of (extracted_text, paragraph_count).
    """
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs), len(paragraphs)


def load_txt(file_bytes: bytes) -> Tuple[str, int]:
    """Extract text from a plain-text file.

    Args:
        file_bytes: Raw bytes of the TXT file.

    Returns:
        Tuple of (extracted_text, line_count).
    """
    text = file_bytes.decode("utf-8", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    return text, len(lines)


def load_document(uploaded_file) -> Tuple[str, str, dict]:
    """Unified dispatcher for Streamlit UploadedFile objects.

    Args:
        uploaded_file: A Streamlit UploadedFile instance.

    Returns:
        Tuple of:
            • raw_text  (str)  — full extracted text
            • filename  (str)  — original filename
            • metadata  (dict) — {source, file_type, size_bytes, pages/paragraphs/lines}
    """
    filename = uploaded_file.name
    file_bytes = uploaded_file.read()
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext == "pdf":
        text, count = load_pdf(file_bytes, filename)
        metadata = {
            "source": filename,
            "file_type": "PDF",
            "size_bytes": len(file_bytes),
            "pages": count,
        }
    elif ext == "docx":
        text, count = load_docx(file_bytes)
        metadata = {
            "source": filename,
            "file_type": "DOCX",
            "size_bytes": len(file_bytes),
            "paragraphs": count,
        }
    elif ext == "txt":
        text, count = load_txt(file_bytes)
        metadata = {
            "source": filename,
            "file_type": "TXT",
            "size_bytes": len(file_bytes),
            "lines": count,
        }
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Please upload PDF, DOCX, or TXT.")

    return text, filename, metadata
