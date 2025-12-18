"""
Configuration for the Physical AI & Humanoid Robotics Textbook RAG system
"""

try:
    from pydantic_settings import BaseSettings as Settings
except ImportError:
    # For older versions of pydantic-settings
    from pydantic import BaseSettings as Settings
from typing import Optional
import os

class RagSettings(Settings):
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

    # Neon Postgres Configuration
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # Embedding Configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # Search Configuration
    search_top_k: int = int(os.getenv("SEARCH_TOP_K", "5"))
    min_relevance_score: float = float(os.getenv("MIN_RELEVANCE_SCORE", "0.3"))

    # Chat Configuration
    max_tokens: int = int(os.getenv("MAX_TOKENS", "500"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Hallucination Prevention Configuration
    hallucination_prevention_enabled: bool = os.getenv("HALLUCINATION_PREVENTION_ENABLED", "true").lower() == "true"
    hallucination_threshold: float = float(os.getenv("HALLUCINATION_THRESHOLD", "0.15"))

    # Textbook-specific settings
    textbook_docs_path: str = os.getenv("TEXTBOOK_DOCS_PATH", "my-website/docs")

# Create a global settings instance
rag_config = RagSettings()