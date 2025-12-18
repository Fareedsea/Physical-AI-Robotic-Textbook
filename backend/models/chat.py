"""
Database models for the Physical AI & Humanoid Robotics Textbook RAG system
Uses SQLAlchemy for Neon Postgres integration
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Import the new config
from rag.new_config import rag_config

Base = declarative_base()

class ChatSession(Base):
    """Model for chat sessions"""
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class ChatMessage(Base):
    """Model for individual chat messages"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_id = Column(String, index=True)
    role = Column(String)  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # For assistant messages, store source information
    sources = Column(Text)  # JSON string of source documents
    confidence = Column(Float)


class ChatFeedback(Base):
    """Model for user feedback on chat responses"""
    __tablename__ = "chat_feedback"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(String, index=True)  # ID of the query being rated
    user_id = Column(String, index=True)
    rating = Column(Integer)  # 1-5 scale
    useful = Column(Boolean)  # Whether the response was useful
    comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class TextbookDocument(Base):
    """Model for textbook documents metadata"""
    __tablename__ = "textbook_documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, unique=True, index=True)  # ID from vector store
    title = Column(String)
    chapter = Column(String)
    section = Column(String)
    relative_path = Column(String)
    content_preview = Column(Text)
    embedding_vector_id = Column(String)  # ID in Qdrant
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SelectedTextContext(Base):
    """Model for user-selected text context"""
    __tablename__ = "selected_text_context"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(String, index=True)
    user_id = Column(String, index=True)
    selected_text = Column(Text)
    selected_text_metadata = Column(Text)  # JSON string of context
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create database engine and session
DATABASE_URL = rag_config.neon_database_url or os.getenv("DATABASE_URL", "sqlite:///./textbook_rag.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    # Create tables when running this file directly
    create_tables()
    print("Database tables created successfully!")