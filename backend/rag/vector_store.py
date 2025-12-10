"""
Vector store implementation for the Physical AI & Humanoid Robotics Textbook RAG system
Uses FAISS for efficient similarity search
"""

import numpy as np
import faiss
import pickle
import logging
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

# Optional imports that might not be available
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    AutoTokenizer = None
    AutoModel = None
    torch = None

logger = logging.getLogger(__name__)

class TextbookVectorStore:
    """Vector store for textbook content using FAISS"""

    def __init__(self,
                 embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 dimension: int = 384,  # Default for MiniLM model
                 index_file: str = "textbook_index.faiss",
                 metadata_file: str = "textbook_metadata.pkl"):
        self.dimension = dimension
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.index = None
        self.metadata = []
        self.doc_ids = []

        if TORCH_AVAILABLE:
            # Initialize embedding model
            self.tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
            self.model = AutoModel.from_pretrained(embedding_model_name)
        else:
            self.tokenizer = None
            self.model = None
            logger.warning("Torch not available, embedding functionality will be limited")

        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity

    def _get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        if not TORCH_AVAILABLE or self.tokenizer is None or self.model is None:
            # Fallback: return random embeddings of correct shape
            # This is just for testing purposes when torch is not available
            logger.warning("Torch not available, returning random embeddings for testing")
            return np.random.rand(len(texts), self.dimension).astype('float32')

        # Tokenize the texts
        encoded_input = self.tokenizer(texts, padding=True, truncation=True,
                                      return_tensors='pt', max_length=512)

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Use mean pooling to get sentence embeddings
            embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings for cosine similarity
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings.cpu().numpy().astype('float32')

    def _mean_pooling(self, model_output, attention_mask):
        """Apply mean pooling to get sentence embeddings"""
        if not TORCH_AVAILABLE:
            # This method should only be called when torch is available
            raise RuntimeError("Torch not available, cannot perform mean pooling")

        token_embeddings = model_output[0]  # First element contains token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store"""
        if not documents:
            return

        # Extract text content and metadata
        texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        doc_ids = [doc['id'] for doc in documents]

        # Generate embeddings
        embeddings = self._get_embeddings(texts)

        # Add embeddings to FAISS index
        self.index.add(embeddings)

        # Store metadata and document IDs
        self.metadata.extend(metadatas)
        self.doc_ids.extend(doc_ids)

        logger.info(f"Added {len(documents)} documents to vector store")

    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Search for similar documents to the query"""
        if self.index.ntotal == 0:
            return []

        # Generate embedding for the query
        query_embedding = self._get_embeddings([query])[0]  # Shape: (dimension,)

        # Perform similarity search
        scores, indices = self.index.search(query_embedding.reshape(1, -1), k)

        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.metadata):  # Valid index check
                doc_info = {
                    'id': self.doc_ids[idx],
                    'metadata': self.metadata[idx],
                    'content': None  # Content not stored in vector store, would need to retrieve from source
                }
                results.append((doc_info, float(score)))

        return results

    def save(self, index_path: Optional[str] = None, metadata_path: Optional[str] = None):
        """Save the vector store to disk"""
        index_path = index_path or self.index_file
        metadata_path = metadata_path or self.metadata_file

        # Save FAISS index
        faiss.write_index(self.index, index_path)

        # Save metadata and doc_ids
        with open(metadata_path, 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'doc_ids': self.doc_ids
            }, f)

        logger.info(f"Vector store saved to {index_path} and {metadata_path}")

    def load(self, index_path: Optional[str] = None, metadata_path: Optional[str] = None):
        """Load the vector store from disk"""
        index_path = index_path or self.index_file
        metadata_path = metadata_path or self.metadata_file

        # Load FAISS index
        self.index = faiss.read_index(index_path)

        # Load metadata and doc_ids
        with open(metadata_path, 'rb') as f:
            data = pickle.load(f)
            self.metadata = data['metadata']
            self.doc_ids = data['doc_ids']

        logger.info(f"Vector store loaded from {index_path} and {metadata_path}")

    def is_empty(self) -> bool:
        """Check if the vector store is empty"""
        return self.index.ntotal == 0

    def is_loaded(self) -> bool:
        """Check if the vector store has been loaded with data"""
        return self.index.ntotal > 0

    def get_document_count(self) -> int:
        """Get the number of documents in the vector store"""
        return self.index.ntotal

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the vector store"""
        documents = []
        for i in range(len(self.metadata)):
            doc_info = {
                'id': self.doc_ids[i],
                'metadata': self.metadata[i]
            }
            documents.append(doc_info)
        return documents


def create_textbook_vector_store(documents: List[Dict[str, Any]],
                                index_file: str = "textbook_index.faiss",
                                metadata_file: str = "textbook_metadata.pkl") -> TextbookVectorStore:
    """Create and populate a vector store with textbook documents"""
    vector_store = TextbookVectorStore(index_file=index_file, metadata_file=metadata_file)

    # Add all documents to the vector store
    vector_store.add_documents(documents)

    # Save the vector store
    vector_store.save()

    return vector_store


if __name__ == "__main__":
    # Example usage
    sample_docs = [
        {
            'id': 'doc1',
            'content': 'Physical AI combines robotics and artificial intelligence to create embodied systems.',
            'metadata': {'title': 'Introduction to Physical AI', 'chapter': 'Chapter 1'}
        },
        {
            'id': 'doc2',
            'content': 'Humanoid robots have multiple degrees of freedom and mimic human movement patterns.',
            'metadata': {'title': 'Humanoid Systems', 'chapter': 'Chapter 3'}
        }
    ]

    # Create vector store
    vs = TextbookVectorStore()
    vs.add_documents(sample_docs)

    # Test search
    results = vs.search("What is Physical AI?", k=2)
    print(f"Search results: {results}")

    # Save the vector store
    vs.save()
    print("Vector store saved successfully")