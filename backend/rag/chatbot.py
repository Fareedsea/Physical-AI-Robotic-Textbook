"""
Chatbot service for the Physical AI & Humanoid Robotics Textbook
Uses LangChain to implement RAG functionality
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from langchain_core.prompts import PromptTemplate
from .vector_store import TextbookVectorStore
from .document_loader import load_textbook_documents
from .search import TextbookSearcher

# Optional imports that might not be available
try:
    from langchain_huggingface import HuggingFacePipeline
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    HuggingFacePipeline = None
    AutoModelForCausalLM = None
    AutoTokenizer = None
    pipeline = None
    torch = None

logger = logging.getLogger(__name__)

class TextbookChatbot:
    """RAG chatbot for textbook content"""

    def __init__(self,
                 vector_store: TextbookVectorStore,
                 model_name: str = "gpt2",  # Using gpt2 as a placeholder; in practice, you'd use a more appropriate model
                 temperature: float = 0.7,
                 max_tokens: int = 500):
        self.vector_store = vector_store
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize the searcher
        self.searcher = TextbookSearcher(vector_store=vector_store)

        # Initialize the LLM
        self.llm = self._initialize_llm()

        # Create a retriever from the vector store
        self.retriever = TextbookRetriever(vector_store)

        # Create the QA chain
        self.qa_chain = self._create_qa_chain()

    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )

            # Set pad token if it doesn't exist
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            # Create text generation pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

            # Create LangChain LLM wrapper
            llm = HuggingFacePipeline(pipeline=pipe)
            return llm
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            # Fallback to a simpler approach for demonstration
            return None

    def _create_qa_chain(self):
        """Create the question answering chain"""
        # Define the prompt template for textbook Q&A
        template = """
        You are an expert assistant for the Physical AI & Humanoid Robotics Textbook.
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context:
        {context}

        Question: {question}

        Helpful Answer:"""

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )

        # In a real implementation, we would use the actual LLM and retriever
        # For this example, we'll create a mock implementation
        return MockQAChain(prompt)

    def get_response(self, query: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a response for the user's query"""
        try:
            # Retrieve relevant documents using the searcher
            search_results = self.searcher.search(query, k=5)

            # Convert search results to documents
            retrieved_docs = []
            for doc_info, score in search_results:
                # Create a mock document object with required attributes
                doc = MockDocument()
                doc.page_content = doc_info['metadata'].get('content', 'Content not available')
                doc.metadata = doc_info['metadata']
                doc.similarity_score = score
                retrieved_docs.append(doc)

            # Generate response using the QA chain
            # In a real implementation, this would call the actual chain
            response_text = self._generate_response(query, retrieved_docs)

            # Format the response
            response = {
                "response": response_text,
                "sources": [doc.metadata for doc in retrieved_docs],
                "confidence": 0.85,  # Placeholder confidence score
                "query_id": f"query_{hash(query) % 1000000}",  # Simple query ID generation
                "user_id": user_id
            }

            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": "Sorry, I encountered an error processing your query. Please try again.",
                "sources": [],
                "confidence": 0.0,
                "query_id": f"error_{hash(query) % 1000000}",
                "user_id": user_id
            }

    def _generate_response(self, query: str, retrieved_docs: List[Any]) -> str:
        """Generate a response based on query and retrieved documents"""
        if not retrieved_docs:
            return "I couldn't find any relevant information in the textbook to answer your question."

        # Combine the content of retrieved documents
        context = " ".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in retrieved_docs[:3]])

        # Simple response generation (in practice, this would use the LLM)
        response = f"Based on the textbook content: {context[:500]}... [truncated for brevity]"
        return response

    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for a user"""
        # This would normally retrieve from a database
        # For now, return an empty list as a placeholder
        return []

    def add_to_history(self, user_id: str, query: str, response: str, sources: List[Dict[str, Any]]):
        """Add a query-response pair to the conversation history"""
        # This would normally save to a database
        # For now, just log it as a placeholder
        logger.info(f"Adding to history for user {user_id}: {query[:50]}...")


class TextbookRetriever:
    """Custom retriever that works with our TextbookVectorStore"""

    def __init__(self, vector_store: TextbookVectorStore):
        self.vector_store = vector_store
        self.searcher = TextbookSearcher(vector_store=vector_store)

    def get_relevant_documents(self, query: str) -> List[Any]:
        """Get relevant documents for a query"""
        results = self.searcher.search(query, k=5)

        # Convert to LangChain-style documents
        documents = []
        for doc_info, score in results:
            # Create a mock document object with required attributes
            doc = MockDocument()
            doc.page_content = doc_info['metadata'].get('content', 'Content not available')
            doc.metadata = doc_info['metadata']
            doc.similarity_score = score
            documents.append(doc)

        return documents


class MockDocument:
    """Mock document class for compatibility with LangChain"""
    def __init__(self):
        self.page_content = ""
        self.metadata = {}
        self.similarity_score = 0.0


class MockQAChain:
    """Mock QA chain for demonstration purposes"""
    def __init__(self, prompt_template):
        self.prompt_template = prompt_template

    def __call__(self, inputs):
        # Mock implementation that returns a simple response
        return {
            "result": f"Mock response to: {inputs.get('query', 'Unknown query')}",
            "source_documents": inputs.get("input_documents", [])
        }


def create_textbook_chatbot(vector_store_path: str = "textbook_index.faiss",
                           metadata_path: str = "textbook_metadata.pkl") -> TextbookChatbot:
    """Create a textbook chatbot with loaded vector store"""
    # Load the vector store
    vector_store = TextbookVectorStore()
    vector_store.load(vector_store_path, metadata_path)

    # Create the chatbot
    chatbot = TextbookChatbot(vector_store=vector_store)

    return chatbot


if __name__ == "__main__":
    # Example usage
    print("Creating textbook chatbot...")

    # This would normally load a pre-built vector store
    # For demonstration, we'll create a minimal one
    from .vector_store import create_textbook_vector_store

    # Load documents
    docs = load_textbook_documents()

    # Create vector store (this would typically be done once and saved)
    if docs:
        vector_store = create_textbook_vector_store(docs)
        chatbot = TextbookChatbot(vector_store=vector_store)

        # Test a query
        response = chatbot.get_response("What is Physical AI?")
        print(f"Response: {response['response']}")
        print(f"Sources: {len(response['sources'])} documents")
    else:
        print("No documents loaded - cannot create chatbot")