"""
utils/embeddings.py — Embedding model factory.

Returns a LangChain-compatible embeddings object based on config:
    • "huggingface" → HuggingFaceEmbeddings (all-MiniLM-L6-v2, free)
    • "openai"      → OpenAIEmbeddings (requires OPENAI_API_KEY)
"""

import config


def get_embeddings():
    """Return the configured embeddings object.

    Returns:
        LangChain Embeddings instance (HuggingFace or OpenAI).

    Raises:
        ValueError: If an unsupported EMBEDDING_PROVIDER is configured.
    """
    provider = config.EMBEDDING_PROVIDER.lower()

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=config.HUGGINGFACE_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    elif provider == "openai":
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Please set it in your .env file or environment variables."
            )
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            api_key=config.OPENAI_API_KEY,
            model="text-embedding-3-small",
        )

    else:
        raise ValueError(
            f"Unsupported EMBEDDING_PROVIDER: '{config.EMBEDDING_PROVIDER}'. "
            "Choose 'huggingface' or 'openai'."
        )
