"""
Chat API endpoints for the Physical AI & Humanoid Robotics Textbook
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
import logging
from datetime import datetime

from rag.chatbot import TextbookChatbot, create_textbook_chatbot
from rag.vector_store import TextbookVectorStore
from rag.search import TextbookSearcher

logger = logging.getLogger(__name__)
router = APIRouter()

# Global chatbot and searcher instances (in production, this would be managed differently)
chatbot: Optional[TextbookChatbot] = None
searcher: Optional[TextbookSearcher] = None


class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    user_id: Optional[str] = Field(None, description="User identifier for tracking")
    session_id: Optional[str] = Field(None, description="Session identifier")
    history: Optional[List[Dict[str, str]]] = Field(None, description="Conversation history")


class ChatQueryResponse(BaseModel):
    response: str = Field(..., description="The chatbot's response")
    sources: List[Dict[str, Any]] = Field(..., description="Sources used to generate the response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the response")
    query_id: str = Field(..., description="Unique identifier for this query")
    user_id: Optional[str] = Field(None, description="User identifier")
    timestamp: str = Field(..., description="Timestamp of the response")


class ChatHistoryRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    limit: int = Field(10, ge=1, le=100, description="Number of history items to return")
    offset: int = Field(0, ge=0, description="Offset for pagination")


class ChatHistoryResponse(BaseModel):
    history: List[Dict[str, Any]] = Field(..., description="List of conversation history items")
    total_count: int = Field(..., description="Total number of history items")
    has_more: bool = Field(..., description="Whether there are more items available")


class ChatFeedbackRequest(BaseModel):
    query_id: str = Field(..., description="ID of the query being rated")
    user_id: Optional[str] = Field(None, description="User identifier")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    useful: Optional[bool] = Field(None, description="Whether the response was useful")
    comment: Optional[str] = Field(None, max_length=1000, description="Additional feedback comment")


class ChatFeedbackResponse(BaseModel):
    success: bool = Field(..., description="Whether feedback was recorded successfully")
    feedback_id: str = Field(..., description="Unique identifier for this feedback")
    message: str = Field(..., description="Status message")


@router.on_event("startup")
async def startup_event():
    """Initialize the chatbot and searcher on startup"""
    global chatbot, searcher
    try:
        # Initialize the vector store
        vector_store = TextbookVectorStore()
        vector_store.load()  # Load from default location

        # Create the searcher instance
        searcher = TextbookSearcher(vector_store=vector_store)

        # Create the chatbot instance
        chatbot = TextbookChatbot(vector_store)
        logger.info("Chatbot and searcher initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot or searcher: {str(e)}")
        chatbot = None
        searcher = None


@router.post("/query", response_model=ChatQueryResponse)
async def query_chatbot(request: ChatQueryRequest):
    """
    Query the textbook chatbot with a question
    """
    global chatbot

    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot service not available")

    try:
        # Get response from chatbot
        response_data = chatbot.get_response(
            query=request.query,
            user_id=request.user_id
        )

        # Add timestamp
        response_data["timestamp"] = datetime.utcnow().isoformat()

        # Add to history
        if request.user_id:
            chatbot.add_to_history(
                user_id=request.user_id,
                query=request.query,
                response=response_data["response"],
                sources=response_data["sources"]
            )

        return ChatQueryResponse(**response_data)

    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing query")


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str, session_id: Optional[str] = None, limit: int = 10, offset: int = 0):
    """
    Get conversation history for a user
    """
    global chatbot

    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot service not available")

    try:
        # Get history from chatbot
        history = chatbot.get_conversation_history(
            user_id=user_id,
            limit=limit
        )

        return ChatHistoryResponse(
            history=history,
            total_count=len(history),
            has_more=False  # Simplified for this example
        )

    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving history")


@router.post("/feedback", response_model=ChatFeedbackResponse)
async def submit_feedback(request: ChatFeedbackRequest):
    """
    Submit feedback for a chat response
    """
    try:
        # In a real implementation, this would save feedback to a database
        # For now, we'll just log it and return success

        feedback_id = f"feedback_{uuid.uuid4().hex[:8]}"
        logger.info(f"Received feedback for query {request.query_id}: rating={request.rating}, useful={request.useful}")

        # Would normally save to database here
        # save_feedback_to_db(request, feedback_id)

        return ChatFeedbackResponse(
            success=True,
            feedback_id=feedback_id,
            message="Feedback recorded successfully"
        )

    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing feedback")


# Initialize chatbot and searcher on module import
def init_chatbot():
    """Initialize chatbot and searcher for use in the API"""
    global chatbot, searcher
    if not chatbot:
        try:
            # Try to load a pre-existing vector store, or create a new one if needed
            vector_store = TextbookVectorStore()
            try:
                vector_store.load()
                logger.info("Loaded existing vector store")
            except:
                logger.info("No existing vector store found, initializing empty one")
                # In a real scenario, you might want to build the vector store here

            # Initialize the searcher
            searcher = TextbookSearcher(vector_store=vector_store)

            chatbot = TextbookChatbot(vector_store)
        except Exception as e:
            logger.error(f"Error initializing chatbot or searcher: {str(e)}")
            chatbot = None
            searcher = None

# Initialize when module is imported
init_chatbot()