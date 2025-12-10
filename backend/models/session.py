"""
Chat session management for the Physical AI & Humanoid Robotics Textbook RAG system
Handles conversation history, user sessions, and chat state persistence
"""

import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import threading
from pathlib import Path


class MessageRole(str, Enum):
    """Role of the message in the conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class ChatMessage:
    """Represents a single chat message"""
    id: str
    role: MessageRole
    content: str
    timestamp: float
    sources: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "sources": self.sources or [],
            "metadata": self.metadata or {}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create from dictionary representation"""
        return cls(
            id=data["id"],
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=data["timestamp"],
            sources=data.get("sources"),
            metadata=data.get("metadata")
        )


@dataclass
class ChatSession:
    """Represents a chat session with conversation history"""
    id: str
    user_id: str
    created_at: float
    updated_at: float
    messages: List[ChatMessage]
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "title": self.title,
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata or {}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatSession':
        """Create from dictionary representation"""
        messages = [ChatMessage.from_dict(msg_data) for msg_data in data["messages"]]
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            messages=messages,
            title=data.get("title"),
            metadata=data.get("metadata")
        )


class SessionStore:
    """Base class for session storage implementations"""

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
        """Create a new chat session"""
        raise NotImplementedError

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        raise NotImplementedError

    def update_session(self, session: ChatSession) -> bool:
        """Update an existing chat session"""
        raise NotImplementedError

    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        raise NotImplementedError

    def get_user_sessions(self, user_id: str, limit: int = 10, offset: int = 0) -> List[ChatSession]:
        """Get all sessions for a user"""
        raise NotImplementedError

    def add_message(self, session_id: str, message: ChatMessage) -> bool:
        """Add a message to a session"""
        raise NotImplementedError


class InMemorySessionStore(SessionStore):
    """In-memory session store for development/testing"""

    def __init__(self):
        self._sessions: Dict[str, ChatSession] = {}
        self._lock = threading.RLock()  # Thread-safe operations

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
        """Create a new chat session"""
        with self._lock:
            session_id = str(uuid.uuid4())
            timestamp = time.time()
            session = ChatSession(
                id=session_id,
                user_id=user_id,
                created_at=timestamp,
                updated_at=timestamp,
                messages=[],
                metadata=metadata
            )
            self._sessions[session_id] = session
            return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        with self._lock:
            return self._sessions.get(session_id)

    def update_session(self, session: ChatSession) -> bool:
        """Update an existing chat session"""
        with self._lock:
            if session.id in self._sessions:
                session.updated_at = time.time()
                self._sessions[session.id] = session
                return True
            return False

    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

    def get_user_sessions(self, user_id: str, limit: int = 10, offset: int = 0) -> List[ChatSession]:
        """Get all sessions for a user"""
        with self._lock:
            user_sessions = [
                session for session in self._sessions.values()
                if session.user_id == user_id
            ]
            # Sort by updated_at (most recent first)
            user_sessions.sort(key=lambda s: s.updated_at, reverse=True)
            return user_sessions[offset:offset + limit]

    def add_message(self, session_id: str, message: ChatMessage) -> bool:
        """Add a message to a session"""
        with self._lock:
            if session_id in self._sessions:
                session = self._sessions[session_id]
                session.messages.append(message)
                session.updated_at = time.time()
                return True
            return False

    def get_session_messages(self, session_id: str, limit: int = 50, offset: int = 0) -> List[ChatMessage]:
        """Get messages from a session"""
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                return session.messages[offset:offset + limit]
            return []


class FileSessionStore(SessionStore):
    """File-based session store for persistence"""

    def __init__(self, storage_dir: str = "backend/data/sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def _get_session_path(self, session_id: str) -> Path:
        """Get the file path for a session"""
        return self.storage_dir / f"{session_id}.json"

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
        """Create a new chat session"""
        with self._lock:
            session_id = str(uuid.uuid4())
            timestamp = time.time()
            session = ChatSession(
                id=session_id,
                user_id=user_id,
                created_at=timestamp,
                updated_at=timestamp,
                messages=[],
                metadata=metadata
            )
            self._save_session(session)
            return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        with self._lock:
            session_path = self._get_session_path(session_id)
            if session_path.exists():
                try:
                    with open(session_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return ChatSession.from_dict(data)
                except (json.JSONDecodeError, KeyError):
                    return None
            return None

    def update_session(self, session: ChatSession) -> bool:
        """Update an existing chat session"""
        with self._lock:
            session.updated_at = time.time()
            return self._save_session(session)

    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        with self._lock:
            session_path = self._get_session_path(session_id)
            if session_path.exists():
                session_path.unlink()
                return True
            return False

    def get_user_sessions(self, user_id: str, limit: int = 10, offset: int = 0) -> List[ChatSession]:
        """Get all sessions for a user"""
        with self._lock:
            all_sessions = []
            for session_file in self.storage_dir.glob("*.json"):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        session = ChatSession.from_dict(data)
                        if session.user_id == user_id:
                            all_sessions.append(session)
                except (json.JSONDecodeError, KeyError):
                    continue

            # Sort by updated_at (most recent first)
            all_sessions.sort(key=lambda s: s.updated_at, reverse=True)
            return all_sessions[offset:offset + limit]

    def add_message(self, session_id: str, message: ChatMessage) -> bool:
        """Add a message to a session"""
        with self._lock:
            session = self.get_session(session_id)
            if session:
                session.messages.append(message)
                session.updated_at = time.time()
                return self._save_session(session)
            return False

    def _save_session(self, session: ChatSession) -> bool:
        """Save a session to file"""
        try:
            session_path = self._get_session_path(session.id)
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False


class ChatSessionManager:
    """Main class for managing chat sessions"""

    def __init__(self, session_store: SessionStore = None):
        self.session_store = session_store or InMemorySessionStore()

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
        """Create a new chat session for a user"""
        return self.session_store.create_session(user_id, metadata)

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        return self.session_store.get_session(session_id)

    def update_session(self, session: ChatSession) -> bool:
        """Update an existing chat session"""
        return self.session_store.update_session(session)

    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        return self.session_store.delete_session(session_id)

    def get_user_sessions(self, user_id: str, limit: int = 10, offset: int = 0) -> List[ChatSession]:
        """Get all sessions for a user"""
        return self.session_store.get_user_sessions(user_id, limit, offset)

    def add_message_to_session(self, session_id: str, role: MessageRole, content: str,
                              sources: Optional[List[Dict[str, Any]]] = None,
                              metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a message to a session"""
        message = ChatMessage(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=time.time(),
            sources=sources,
            metadata=metadata
        )
        return self.session_store.add_message(session_id, message)

    def get_session_history(self, session_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        session = self.session_store.get_session(session_id)
        if session:
            messages = session.messages[offset:offset + limit]
            return [msg.to_dict() for msg in messages]
        return []

    def get_user_conversation_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent conversation history across all of a user's sessions"""
        # Get user's sessions
        user_sessions = self.session_store.get_user_sessions(user_id, limit=10)

        # Collect recent messages from all sessions
        all_messages = []
        for session in user_sessions:
            for msg in session.messages[-5:]:  # Last 5 messages from each session
                all_messages.append({
                    "session_id": session.id,
                    "session_title": session.title,
                    "message": msg.to_dict()
                })

        # Sort by timestamp (most recent first)
        all_messages.sort(key=lambda x: x["message"]["timestamp"], reverse=True)
        return all_messages[:limit]


# Global session manager instance
_session_manager: Optional[ChatSessionManager] = None


def get_session_manager() -> ChatSessionManager:
    """Get the global session manager instance"""
    global _session_manager
    if _session_manager is None:
        # Use file-based storage for persistence
        session_store = FileSessionStore()
        _session_manager = ChatSessionManager(session_store)
    return _session_manager


def create_session(user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
    """Create a new chat session for a user"""
    manager = get_session_manager()
    return manager.create_session(user_id, metadata)


def get_session(session_id: str) -> Optional[ChatSession]:
    """Get a chat session by ID"""
    manager = get_session_manager()
    return manager.get_session(session_id)


def add_message_to_session(session_id: str, role: MessageRole, content: str,
                         sources: Optional[List[Dict[str, Any]]] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> bool:
    """Add a message to a session"""
    manager = get_session_manager()
    return manager.add_message_to_session(session_id, role, content, sources, metadata)


if __name__ == "__main__":
    # Example usage
    print("Testing chat session management...")

    # Create a session manager
    manager = ChatSessionManager()

    # Create a new session for a user
    user_session = manager.create_session("user_123", {"device": "web", "locale": "en"})
    print(f"Created session: {user_session.id}")

    # Add some messages to the session
    manager.add_message_to_session(
        user_session.id,
        MessageRole.USER,
        "What is Physical AI?"
    )

    manager.add_message_to_session(
        user_session.id,
        MessageRole.ASSISTANT,
        "Physical AI combines robotics and artificial intelligence to create embodied systems that interact with the physical world.",
        sources=[{"title": "Introduction to Physical AI", "chapter": "Chapter 1"}]
    )

    # Get the session history
    history = manager.get_session_history(user_session.id)
    print(f"Session has {len(history)} messages")

    # Get user's sessions
    user_sessions = manager.get_user_sessions("user_123")
    print(f"User has {len(user_sessions)} sessions")