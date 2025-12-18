"""
OpenAI-based RAG chatbot for the Physical AI & Humanoid Robotics Textbook
Uses OpenAI API, Qdrant for vector storage, and Neon Postgres for metadata
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document as LCDocument
import openai
from datetime import datetime
import json

from rag.new_config import rag_config
from rag.qdrant_store import QdrantTextbookStore
from models.chat import ChatMessage, ChatSession, ChatFeedback, SelectedTextContext, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class OpenAITextbookChatbot:
    """RAG chatbot using OpenAI API for textbook content"""

    def __init__(self,
                 qdrant_store: QdrantTextbookStore,
                 db_session: Session = None):
        self.qdrant_store = qdrant_store
        self.db_session = db_session or next(get_db())  # Default session if not provided

        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model=rag_config.openai_model,
            temperature=rag_config.temperature,
            max_tokens=rag_config.max_tokens,
            api_key=rag_config.openai_api_key
        )

        # Create the QA chain
        self.qa_chain = self._create_qa_chain()

    def _create_qa_chain(self):
        """Create the question answering chain with RAG"""
        template = """
        You are an expert assistant for the Physical AI & Humanoid Robotics Textbook.
        Use only the following pieces of context to answer the question at the end.
        If you don't know the answer based on the provided context, just say that you don't know, don't try to make up an answer.
        Be concise and accurate in your response.

        Context:
        {context}

        Question: {question}

        Helpful Answer:"""

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )

        # Create the chain
        chain = (
            {
                "context": lambda x: self._format_context(x["retrieved_docs"]),
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain

    def _format_context(self, retrieved_docs: List[Tuple[Dict[str, Any], float]]) -> str:
        """Format retrieved documents into context string"""
        if not retrieved_docs:
            return "No relevant information found in the textbook."

        context_parts = []
        for doc_info, score in retrieved_docs:
            metadata = doc_info['metadata']
            content = doc_info['content'][:1000]  # Limit content length
            source_info = f"Chapter: {metadata.get('chapter', 'N/A')}, Section: {metadata.get('section', 'N/A')}"
            context_parts.append(f"[Source: {source_info}]\n{content}\n")

        return "\n".join(context_parts)

    def get_response(self,
                     query: str,
                     user_id: Optional[str] = None,
                     session_id: Optional[str] = None,
                     history: Optional[List[Dict[str, str]]] = None,
                     selected_text: Optional[str] = None) -> Dict[str, Any]:
        """Get a response for the user's query"""
        try:
            # Search for relevant documents
            if selected_text:
                # If user has selected specific text, search within that context
                search_results = self.qdrant_store.search_with_selected_text(
                    query, selected_text, k=rag_config.search_top_k
                )

                # Also save the selected text context for future reference
                self._save_selected_text_context(query, user_id, selected_text)
            else:
                # Standard search across all textbook content
                search_results = self.qdrant_store.search(
                    query, k=rag_config.search_top_k, min_relevance=rag_config.min_relevance_score
                )

            # Prepare context from search results
            context_docs = [doc_info for doc_info, _ in search_results]

            # Format the context for the LLM
            context_str = self._format_context(search_results)

            # Prepare the full prompt with context
            if history:
                # Include conversation history if provided
                history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
                full_query = f"Previous conversation:\n{history_str}\n\nCurrent question: {query}"
            else:
                full_query = query

            # Generate response using the QA chain
            response_text = self.qa_chain.invoke({
                "retrieved_docs": search_results,
                "question": full_query
            })

            # Calculate average confidence from retrieved documents
            confidence = sum([score for _, score in search_results]) / len(search_results) if search_results else 0.0

            # Apply hallucination prevention
            context_str = self._format_context(search_results)
            response_text = self._verify_and_correct_response(full_query, response_text, context_str)

            # Prepare sources information
            sources = []
            for doc_info, score in search_results:
                metadata = doc_info['metadata']
                source_info = {
                    'id': doc_info['id'],
                    'title': metadata.get('title', 'Untitled'),
                    'chapter': metadata.get('chapter', 'Unknown'),
                    'section': metadata.get('section', ''),
                    'relative_path': metadata.get('relative_path', ''),
                    'similarity_score': score
                }
                sources.append(source_info)

            # Prepare response
            response = {
                "response": response_text,
                "sources": sources,
                "confidence": min(confidence, 1.0),  # Ensure confidence is between 0 and 1
                "query_id": f"query_{hash(query + str(datetime.utcnow())) % 1000000}",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Save to database
            self._save_chat_message(user_id, session_id, "user", query)
            self._save_chat_message(user_id, session_id, "assistant", response_text, sources, confidence)

            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": "Sorry, I encountered an error processing your query. Please try again.",
                "sources": [],
                "confidence": 0.0,
                "query_id": f"error_{hash(query) % 1000000}",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }

    def _save_chat_message(self,
                          user_id: Optional[str],
                          session_id: Optional[str],
                          role: str,
                          content: str,
                          sources: List[Dict[str, Any]] = None,
                          confidence: float = None):
        """Save chat message to database"""
        try:
            message = ChatMessage(
                session_id=session_id,
                user_id=user_id,
                role=role,
                content=content,
                sources=json.dumps(sources) if sources else None,
                confidence=confidence
            )
            self.db_session.add(message)
            self.db_session.commit()
        except Exception as e:
            logger.error(f"Error saving chat message to database: {str(e)}")
            self.db_session.rollback()

    def _save_selected_text_context(self, query: str, user_id: Optional[str], selected_text: str):
        """Save selected text context to database"""
        try:
            context = SelectedTextContext(
                query_id=f"query_{hash(query) % 1000000}",
                user_id=user_id,
                selected_text=selected_text,
                selected_text_metadata=json.dumps({"timestamp": datetime.utcnow().isoformat()})
            )
            self.db_session.add(context)
            self.db_session.commit()
        except Exception as e:
            logger.error(f"Error saving selected text context to database: {str(e)}")
            self.db_session.rollback()

    def get_conversation_history(self, user_id: str, session_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for a user"""
        try:
            query = self.db_session.query(ChatMessage).filter(ChatMessage.user_id == user_id)

            if session_id:
                query = query.filter(ChatMessage.session_id == session_id)

            messages = query.order_by(ChatMessage.timestamp.desc()).limit(limit).all()

            # Convert to dictionary format
            history = []
            for msg in reversed(messages):  # Reverse to get chronological order
                history.append({
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
                    'sources': json.loads(msg.sources) if msg.sources else None,
                    'confidence': msg.confidence
                })

            return history
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {str(e)}")
            return []

    def submit_feedback(self, query_id: str, user_id: Optional[str], rating: Optional[int],
                       useful: Optional[bool], comment: Optional[str]) -> Dict[str, Any]:
        """Submit feedback for a query response"""
        try:
            feedback = ChatFeedback(
                query_id=query_id,
                user_id=user_id,
                rating=rating,
                useful=useful,
                comment=comment
            )
            self.db_session.add(feedback)
            self.db_session.commit()

            return {
                "success": True,
                "feedback_id": f"feedback_{hash(str(query_id) + str(user_id) + str(datetime.utcnow())) % 1000000}",
                "message": "Feedback recorded successfully"
            }
        except Exception as e:
            logger.error(f"Error saving feedback to database: {str(e)}")
            self.db_session.rollback()
            return {
                "success": False,
                "feedback_id": None,
                "message": "Error recording feedback"
            }

    def verify_response_from_context(self, query: str, response: str, context: str) -> Tuple[bool, Dict[str, Any]]:
        """Verify that the response is grounded in the provided context (hallucination prevention)"""
        verification_result = {
            "is_grounding_valid": False,
            "confidence_score": 0.0,
            "details": {}
        }

        if not context.strip() or not response.strip():
            verification_result["details"]["error"] = "Empty context or response"
            return False, verification_result

        response_lower = response.lower()
        context_lower = context.lower()
        query_lower = query.lower()

        # 1. Check semantic overlap using sentence transformers (if available)
        try:
            from sentence_transformers import util
            import torch

            # Create embeddings for verification
            model = SentenceTransformer(rag_config.embedding_model)
            response_embedding = model.encode(response, convert_to_tensor=True)
            context_embedding = model.encode(context, convert_to_tensor=True)
            query_embedding = model.encode(query, convert_to_tensor=True)

            # Calculate cosine similarity
            response_context_sim = util.cos_sim(response_embedding, context_embedding).item()
            query_context_sim = util.cos_sim(query_embedding, context_embedding).item()

            verification_result["details"]["response_context_similarity"] = response_context_sim
            verification_result["details"]["query_context_similarity"] = query_context_sim

        except Exception as e:
            # Fallback to simple word overlap if sentence transformers not available
            context_words = set(context_lower.split())
            response_words = set(response_lower.split())
            query_words = set(query_lower.split())

            # Calculate word overlap ratios
            response_context_overlap = len(context_words.intersection(response_words))
            query_context_overlap = len(context_words.intersection(query_words))

            response_total = len(response_words)
            context_total = len(context_words)
            query_total = len(query_words)

            response_context_ratio = response_context_overlap / max(response_total, 1)
            query_context_ratio = query_context_overlap / max(query_total, 1)
            context_response_ratio = response_context_overlap / max(context_total, 1)

            verification_result["details"]["response_context_word_ratio"] = response_context_ratio
            verification_result["details"]["query_context_word_ratio"] = query_context_ratio
            verification_result["details"]["context_response_word_ratio"] = context_response_ratio

            # Calculate overall confidence score
            # Weight context-response overlap more heavily
            score = (context_response_ratio * 0.6) + (response_context_ratio * 0.3) + (query_context_ratio * 0.1)
            verification_result["confidence_score"] = min(score, 1.0)

            # Consider grounded if there's reasonable overlap
            verification_result["is_grounding_valid"] = score > 0.1

        # 2. Check for hallucinated facts (responses containing specific claims not in context)
        # Look for specific indicators of hallucination
        hallucination_indicators = [
            "according to the textbook",
            "the book states",
            "as mentioned in the text",
            "the text says",
            # Check for specific claims that might not be in context
        ]

        # Count how many indicators are in response but not well-supported by context
        response_indicators = [indicator for indicator in hallucination_indicators if indicator in response_lower]
        context_indicators = [indicator for indicator in hallucination_indicators if indicator in context_lower]

        verification_result["details"]["response_indicators"] = response_indicators
        verification_result["details"]["context_indicators"] = context_indicators

        # 3. Additional checks for consistency
        # Check if response is too generic or doesn't address the query
        query_in_response = len([word for word in query_words if word in response_words]) / max(len(query_words), 1)
        verification_result["details"]["query_coverage_in_response"] = query_in_response

        # Final verification: response should be relevant to both query and context
        threshold = rag_config.hallucination_threshold
        if verification_result["confidence_score"] > threshold and query_in_response > 0.1:
            verification_result["is_grounding_valid"] = True

        return verification_result["is_grounding_valid"], verification_result

    def _verify_and_correct_response(self, query: str, response: str, context: str) -> str:
        """Verify response and potentially correct hallucinations"""
        if not rag_config.hallucination_prevention_enabled:
            return response

        is_valid, verification_details = self.verify_response_from_context(query, response, context)

        if not is_valid:
            # If response is not well-grounded, provide a safer fallback
            logger.warning(f"Response failed hallucination check: {verification_details}")
            return ("I couldn't find specific information in the textbook to answer your question. "
                   "The response might not be fully supported by the provided context. "
                   "Please refer to the textbook chapters for accurate information.")

        return response


def create_openai_chatbot(qdrant_store: QdrantTextbookStore = None,
                         db_session: Session = None) -> OpenAITextbookChatbot:
    """Create an OpenAI textbook chatbot instance"""
    if not qdrant_store:
        qdrant_store = QdrantTextbookStore()

    return OpenAITextbookChatbot(qdrant_store=qdrant_store, db_session=db_session)


if __name__ == "__main__":
    # Example usage
    print("Creating OpenAI textbook chatbot...")

    # Create Qdrant store
    qdrant_store = QdrantTextbookStore()

    # Create chatbot
    chatbot = OpenAITextbookChatbot(qdrant_store=qdrant_store)

    # Test a query
    response = chatbot.get_response("What is Physical AI?", user_id="test_user")
    print(f"Response: {response['response']}")
    print(f"Sources: {len(response['sources'])} documents")
    print(f"Confidence: {response['confidence']:.3f}")