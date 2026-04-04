"""
Context Management - Auto-compression and optimization
"""

from dataclasses import dataclass
from typing import Any

from yanzhiti.types import AssistantMessage, Message, UserMessage


@dataclass
class CompressionStats:
    """Statistics for compression operation"""

    original_messages: int
    compressed_messages: int
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float


class ContextCompressor:
    """
    Compresses conversation context to fit within token limits
    """

    def __init__(
        self,
        max_tokens: int = 128000,  # AI model's context window
        target_tokens: int = 100000,  # Target after compression
        preserve_recent: int = 5,  # Always keep last N messages
    ):
        self.max_tokens = max_tokens
        self.target_tokens = target_tokens
        self.preserve_recent = preserve_recent

    def estimate_tokens(self, messages: list[Message]) -> int:
        """Estimate token count for messages"""
        # Simple estimation: ~4 characters per token
        total_chars = 0
        for msg in messages:
            content = msg.content if isinstance(msg.content, str) else str(msg.content)
            total_chars += len(content)

        return total_chars // 4

    def should_compress(self, messages: list[Message]) -> bool:
        """Check if compression is needed"""
        token_count = self.estimate_tokens(messages)
        return token_count > self.target_tokens

    async def compress(
        self,
        messages: list[Message],
        strategy: str = "sliding_window",
    ) -> tuple[list[Message], CompressionStats]:
        """
        Compress messages using specified strategy

        Strategies:
        - sliding_window: Keep recent messages
        - summarize: Summarize old messages
        - semantic: Keep semantically important messages
        """
        original_tokens = self.estimate_tokens(messages)
        original_count = len(messages)

        if strategy == "sliding_window":
            compressed = await self._compress_sliding_window(messages)
        elif strategy == "summarize":
            compressed = await self._compress_summarize(messages)
        elif strategy == "semantic":
            compressed = await self._compress_semantic(messages)
        else:
            compressed = messages

        compressed_tokens = self.estimate_tokens(compressed)
        compressed_count = len(compressed)

        stats = CompressionStats(
            original_messages=original_count,
            compressed_messages=compressed_count,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / original_tokens if original_tokens > 0 else 0,
        )

        return compressed, stats

    async def _compress_sliding_window(self, messages: list[Message]) -> list[Message]:
        """Keep most recent messages"""
        if len(messages) <= self.preserve_recent:
            return messages

        # Keep system message if present
        system_messages = [m for m in messages if m.role.value == "system"]
        other_messages = [m for m in messages if m.role.value != "system"]

        # Keep recent messages
        recent = other_messages[-self.preserve_recent :]

        # Add compression notice
        removed_count = len(other_messages) - len(recent)
        if removed_count > 0:
            notice = UserMessage(
                content=f"[Context compressed: {removed_count} earlier messages removed]"
            )
            return system_messages + [notice] + recent

        return system_messages + recent

    async def _compress_summarize(self, messages: list[Message]) -> list[Message]:
        """Summarize old messages (requires LLM)"""
        # For now, fall back to sliding window
        # Full implementation would use LLM to summarize
        return await self._compress_sliding_window(messages)

    async def _compress_semantic(self, messages: list[Message]) -> list[Message]:
        """Keep semantically important messages"""
        # For now, fall back to sliding window
        # Full implementation would use embeddings to find important messages
        return await self._compress_sliding_window(messages)


class ContextManager:
    """
    High-level context management
    """

    def __init__(
        self,
        max_tokens: int = 128000,
        auto_compress: bool = True,
        compression_threshold: float = 0.8,  # Compress at 80% of max
    ):
        self.max_tokens = max_tokens
        self.auto_compress = auto_compress
        self.compression_threshold = compression_threshold
        self.compressor = ContextCompressor(max_tokens=max_tokens)
        self.messages: list[Message] = []
        self._compression_count = 0

    def add_message(self, message: Message):
        """Add a message to context"""
        self.messages.append(message)

    def get_messages(self) -> list[Message]:
        """Get all messages"""
        return self.messages

    def clear(self):
        """Clear all messages"""
        self.messages.clear()

    async def maybe_compress(self) -> CompressionStats | None:
        """Compress if needed"""
        if not self.auto_compress:
            return None

        token_count = self.compressor.estimate_tokens(self.messages)
        threshold_tokens = int(self.max_tokens * self.compression_threshold)

        if token_count > threshold_tokens:
            compressed, stats = await self.compressor.compress(self.messages)
            self.messages = compressed
            self._compression_count += 1
            return stats

        return None

    def get_stats(self) -> dict[str, Any]:
        """Get context statistics"""
        token_count = self.compressor.estimate_tokens(self.messages)
        return {
            "message_count": len(self.messages),
            "token_count": token_count,
            "max_tokens": self.max_tokens,
            "utilization": token_count / self.max_tokens,
            "compression_count": self._compression_count,
        }


class MessagePrioritizer:
    """
    Prioritizes messages for context management
    """

    def __init__(self):
        self._important_keywords = {
            "error",
            "exception",
            "fail",
            "bug",
            "fix",
            "important",
            "critical",
            "warning",
            "note",
            "todo",
            "fixme",
            "hack",
        }

    def calculate_importance(self, message: Message) -> float:
        """Calculate importance score for a message (0-1)"""
        content = message.content if isinstance(message.content, str) else str(message.content)
        content_lower = content.lower()

        score = 0.0

        # Check for important keywords
        for keyword in self._important_keywords:
            if keyword in content_lower:
                score += 0.1

        # User messages are slightly more important
        if message.role.value == "user":
            score += 0.2

        # Longer messages might be more important
        if len(content) > 500:
            score += 0.1

        # Cap at 1.0
        return min(score, 1.0)

    def prioritize(self, messages: list[Message]) -> list[tuple[Message, float]]:
        """Prioritize messages by importance"""
        scored = [(msg, self.calculate_importance(msg)) for msg in messages]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


class ContextOptimizer:
    """
    Optimizes context for better model performance
    """

    def __init__(self):
        self.prioritizer = MessagePrioritizer()

    def optimize(self, messages: list[Message]) -> list[Message]:
        """Optimize message order and content"""
        # Remove duplicate consecutive messages
        messages = self._remove_duplicates(messages)

        # Merge short consecutive messages
        messages = self._merge_short_messages(messages)

        return messages

    def _remove_duplicates(self, messages: list[Message]) -> list[Message]:
        """Remove duplicate consecutive messages"""
        if len(messages) < 2:
            return messages

        result = [messages[0]]
        for msg in messages[1:]:
            last = result[-1]
            if msg.role == last.role and msg.content == last.content:
                continue
            result.append(msg)

        return result

    def _merge_short_messages(self, messages: list[Message]) -> list[Message]:
        """Merge short consecutive messages from same role"""
        if len(messages) < 2:
            return messages

        result = []
        current_group = [messages[0]]

        for msg in messages[1:]:
            last = current_group[-1]

            # Check if we should merge
            last_content = last.content if isinstance(last.content, str) else str(last.content)
            msg_content = msg.content if isinstance(msg.content, str) else str(msg.content)

            if msg.role == last.role and len(last_content) < 100 and len(msg_content) < 100:
                current_group.append(msg)
            else:
                # Flush current group
                if len(current_group) == 1:
                    result.append(current_group[0])
                else:
                    # Merge group
                    merged_content = "\n".join(
                        m.content if isinstance(m.content, str) else str(m.content)
                        for m in current_group
                    )
                    merged = (
                        UserMessage(content=merged_content)
                        if current_group[0].role.value == "user"
                        else AssistantMessage(content=merged_content)
                    )
                    result.append(merged)

                current_group = [msg]

        # Flush last group
        if len(current_group) == 1:
            result.append(current_group[0])
        else:
            merged_content = "\n".join(
                m.content if isinstance(m.content, str) else str(m.content) for m in current_group
            )
            merged = (
                UserMessage(content=merged_content)
                if current_group[0].role.value == "user"
                else AssistantMessage(content=merged_content)
            )
            result.append(merged)

        return result
