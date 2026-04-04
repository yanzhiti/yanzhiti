"""
Session Management - Persistence and resume functionality
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from yanzhiti.types import AssistantMessage, Message, UserMessage


class SessionMetadata(BaseModel):
    """Session metadata"""
    session_id: str
    created_at: datetime
    updated_at: datetime
    model: str
    backend: str
    message_count: int = 0
    total_tokens: int = 0
    tags: list[str] = Field(default_factory=list)


class Session(BaseModel):
    """A complete session with messages and metadata"""
    metadata: SessionMetadata
    messages: list[dict[str, Any]] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)


class SessionStorage:
    """
    Storage for session persistence
    Uses JSONL format for efficient append operations
    """

    def __init__(self, storage_dir: Path | None = None):
        if storage_dir is None:
            # Default storage location
            home = Path.home()
            storage_dir = home / ".yanzhiti" / "sessions"

        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_file(self, session_id: str) -> Path:
        """Get the file path for a session"""
        return self.storage_dir / f"{session_id}.jsonl"

    def _get_metadata_file(self, session_id: str) -> Path:
        """Get the metadata file path"""
        return self.storage_dir / f"{session_id}.meta.json"

    async def save_session(self, session: Session):
        """Save a complete session"""
        # Save metadata
        meta_file = self._get_metadata_file(session.metadata.session_id)
        meta_file.write_text(session.metadata.model_dump_json(indent=2))

        # Save messages in JSONL format
        session_file = self._get_session_file(session.metadata.session_id)
        with open(session_file, 'w') as f:
            for msg in session.messages:
                f.write(json.dumps(msg) + '\n')

    async def load_session(self, session_id: str) -> Session | None:
        """Load a session by ID"""
        meta_file = self._get_metadata_file(session_id)
        session_file = self._get_session_file(session_id)

        if not meta_file.exists() or not session_file.exists():
            return None

        # Load metadata
        metadata = SessionMetadata.model_validate_json(meta_file.read_text())

        # Load messages
        messages = []
        with open(session_file) as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))

        return Session(
            metadata=metadata,
            messages=messages,
        )

    async def append_message(self, session_id: str, message: Message):
        """Append a message to an existing session"""
        session_file = self._get_session_file(session_id)

        # Convert message to dict
        msg_dict = {
            "role": message.role.value,
            "content": message.content if isinstance(message.content, str) else str(message.content),
            "timestamp": datetime.now().isoformat(),
        }

        # Append to file
        with open(session_file, 'a') as f:
            f.write(json.dumps(msg_dict) + '\n')

        # Update metadata
        meta_file = self._get_metadata_file(session_id)
        if meta_file.exists():
            metadata = SessionMetadata.model_validate_json(meta_file.read_text())
            metadata.message_count += 1
            metadata.updated_at = datetime.now()
            meta_file.write_text(metadata.model_dump_json(indent=2))

    async def list_sessions(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> list[SessionMetadata]:
        """List all sessions"""
        sessions = []

        for meta_file in self.storage_dir.glob("*.meta.json"):
            try:
                metadata = SessionMetadata.model_validate_json(meta_file.read_text())
                sessions.append(metadata)
            except Exception:
                continue

        # Sort by updated_at (most recent first)
        sessions.sort(key=lambda s: s.updated_at, reverse=True)

        return sessions[offset:offset + limit]

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        meta_file = self._get_metadata_file(session_id)
        session_file = self._get_session_file(session_id)

        deleted = False

        if meta_file.exists():
            meta_file.unlink()
            deleted = True

        if session_file.exists():
            session_file.unlink()
            deleted = True

        return deleted

    async def search_sessions(self, query: str) -> list[SessionMetadata]:
        """Search sessions by content"""
        results = []

        for meta_file in self.storage_dir.glob("*.meta.json"):
            try:
                metadata = SessionMetadata.model_validate_json(meta_file.read_text())
                session_id = metadata.session_id
                session_file = self._get_session_file(session_id)

                # Search in messages
                if session_file.exists():
                    with open(session_file) as f:
                        for line in f:
                            if query.lower() in line.lower():
                                results.append(metadata)
                                break
            except Exception:
                continue

        return results


class SessionManager:
    """
    High-level session manager
    """

    def __init__(self, storage_dir: Path | None = None):
        self.storage = SessionStorage(storage_dir)
        self.current_session: Session | None = None

    async def create_session(
        self,
        model: str,
        backend: str,
        config: dict[str, Any] | None = None,
    ) -> Session:
        """Create a new session"""
        session_id = str(uuid4())
        now = datetime.now()

        metadata = SessionMetadata(
            session_id=session_id,
            created_at=now,
            updated_at=now,
            model=model,
            backend=backend,
        )

        session = Session(
            metadata=metadata,
            messages=[],
            config=config or {},
        )

        await self.storage.save_session(session)
        self.current_session = session

        return session

    async def resume_session(self, session_id: str) -> Session | None:
        """Resume an existing session"""
        session = await self.storage.load_session(session_id)

        if session:
            self.current_session = session

        return session

    async def add_message(self, message: Message):
        """Add a message to current session"""
        if not self.current_session:
            raise RuntimeError("No active session")

        # Add to session
        msg_dict = {
            "role": message.role.value,
            "content": message.content if isinstance(message.content, str) else str(message.content),
            "timestamp": datetime.now().isoformat(),
        }
        self.current_session.messages.append(msg_dict)

        # Persist
        await self.storage.append_message(
            self.current_session.metadata.session_id,
            message
        )

    async def save_current_session(self):
        """Save the current session"""
        if self.current_session:
            self.current_session.metadata.updated_at = datetime.now()
            await self.storage.save_session(self.current_session)

    async def list_sessions(self, limit: int = 20) -> list[SessionMetadata]:
        """List recent sessions"""
        return await self.storage.list_sessions(limit=limit)

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if self.current_session and self.current_session.metadata.session_id == session_id:
            self.current_session = None

        return await self.storage.delete_session(session_id)

    async def search_sessions(self, query: str) -> list[SessionMetadata]:
        """Search sessions"""
        return await self.storage.search_sessions(query)

    def get_session_messages(self) -> list[Message]:
        """Get messages from current session as Message objects"""
        if not self.current_session:
            return []

        messages = []
        for msg_dict in self.current_session.messages:
            role = msg_dict.get("role", "user")
            content = msg_dict.get("content", "")

            if role == "user":
                messages.append(UserMessage(content=content))
            elif role == "assistant":
                messages.append(AssistantMessage(content=content))

        return messages
