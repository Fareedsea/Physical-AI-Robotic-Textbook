"""
Configuration for the Physical AI & Humanoid Robotics Textbook RAG system
Contains settings for embedding models, vector stores, and other RAG components
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os


@dataclass
class EmbeddingConfig:
    """Configuration for embedding models"""
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_seq_length: int = 512
    embedding_dim: int = 384
    batch_size: int = 16
    normalize_embeddings: bool = True


@dataclass
class VectorStoreConfig:
    """Configuration for vector store"""
    index_file: str = "textbook_index.faiss"
    metadata_file: str = "textbook_metadata.pkl"
    similarity_metric: str = "cosine"  # Options: "cosine", "euclidean", "dot_product
    search_k: int = 5  # Number of results to retrieve
    ef_search: int = 64  # For HNSW indices


@dataclass
class RAGConfig:
    """Main configuration for the RAG system"""
    # Embedding configuration
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)

    # Vector store configuration
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)

    # Chatbot configuration
    temperature: float = 0.7
    max_tokens: int = 500
    top_p: float = 0.9
    top_k: int = 50

    # Content processing
    chunk_size: int = 512  # Characters per chunk
    chunk_overlap: int = 50  # Overlap between chunks
    min_content_length: int = 50  # Minimum length for content to be indexed

    # File paths
    docs_path: str = "my-website/docs"
    index_path: str = "backend/data/textbook_index.faiss"
    metadata_path: str = "backend/data/textbook_metadata.pkl"

    # Model cache
    model_cache_dir: Optional[str] = None

    def __post_init__(self):
        """Set up configuration after initialization"""
        # Set cache directory if not provided
        if self.model_cache_dir is None:
            self.model_cache_dir = os.getenv("HF_HOME", os.path.expanduser("~/.cache/huggingface"))

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)


@dataclass
class SearchConfig:
    """Configuration for search functionality"""
    max_results: int = 10
    min_relevance_score: float = 0.3
    use_hybrid_search: bool = False  # Whether to combine semantic and keyword search
    keyword_weight: float = 0.3  # Weight for keyword matching in hybrid search
    semantic_weight: float = 0.7  # Weight for semantic matching in hybrid search


# Global configuration instance
rag_config = RAGConfig()
search_config = SearchConfig()


def get_config() -> RAGConfig:
    """Get the global RAG configuration"""
    return rag_config


def get_search_config() -> SearchConfig:
    """Get the global search configuration"""
    return search_config


# Environment-specific configuration
def get_config_from_env() -> RAGConfig:
    """Create configuration from environment variables"""
    config = RAGConfig()

    # Override with environment variables if present
    if os.getenv("EMBEDDING_MODEL"):
        config.embedding.model_name = os.getenv("EMBEDDING_MODEL")

    if os.getenv("MAX_TOKENS"):
        config.max_tokens = int(os.getenv("MAX_TOKENS"))

    if os.getenv("TEMPERATURE"):
        config.temperature = float(os.getenv("TEMPERATURE"))

    if os.getenv("DOCS_PATH"):
        config.docs_path = os.getenv("DOCS_PATH")

    if os.getenv("INDEX_PATH"):
        config.index_path = os.getenv("INDEX_PATH")

    if os.getenv("METADATA_PATH"):
        config.metadata_path = os.getenv("METADATA_PATH")

    return config


# Initialize configuration from environment
config = get_config_from_env()


if __name__ == "__main__":
    # Test configuration
    print("RAG Configuration:")
    print(f"  Embedding Model: {config.embedding.model_name}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    print(f"  Docs Path: {config.docs_path}")
    print(f"  Index Path: {config.index_path}")