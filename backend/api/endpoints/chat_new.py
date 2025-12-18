"""
Updated Chat API endpoints for the Physical AI & Humanoid Robotics Textbook
Uses OpenAI, Qdrant, and Neon Postgres
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from rag.openai_chatbot import OpenAITextbookChatbot, create_openai_chatbot
from rag.qdrant_store import QdrantTextbookStore
from models.chat import get_db

logger = logging.getLogger(__name__)
router = APIRouter()

# Global chatbot instance
chatbot: Optional[OpenAITextbookChatbot] = None


class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    user_id: Optional[str] = Field(None, description="User identifier for tracking")
    session_id: Optional[str] = Field(None, description="Session identifier")
    history: Optional[List[Dict[str, str]]] = Field(None, description="Conversation history")
    selected_text: Optional[str] = Field(None, description="User-selected text for grounding")


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
    """Initialize the chatbot on startup"""
    global chatbot
    try:
        # Initialize the Qdrant store
        qdrant_store = QdrantTextbookStore()

        # Create the chatbot instance
        chatbot = create_openai_chatbot(qdrant_store=qdrant_store)
        logger.info("OpenAI Chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {str(e)}")
        chatbot = None


@router.post("/query", response_model=ChatQueryResponse)
async def query_chatbot(request: ChatQueryRequest, db: Session = Depends(get_db)):
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
            user_id=request.user_id,
            session_id=request.session_id,
            history=request.history,
            selected_text=request.selected_text
        )

        return ChatQueryResponse(**response_data)

    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing query")


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str, session_id: Optional[str] = None, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
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
            session_id=session_id,
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
async def submit_feedback(request: ChatFeedbackRequest, db: Session = Depends(get_db)):
    """
    Submit feedback for a chat response
    """
    global chatbot

    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot service not available")

    try:
        # Submit feedback to chatbot
        result = chatbot.submit_feedback(
            query_id=request.query_id,
            user_id=request.user_id,
            rating=request.rating,
            useful=request.useful,
            comment=request.comment
        )

        return ChatFeedbackResponse(**result)

    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing feedback")