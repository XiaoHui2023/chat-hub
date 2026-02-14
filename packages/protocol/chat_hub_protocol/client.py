"""客户端便捷函数。

封装 ChatPayload / CommandPayload 的构建过程，
让调用方一行代码即可生成可序列化的请求载荷。
"""

from __future__ import annotations

from .chat import ChatPayload, Message, Role
from .command import (
    ClearContextCommand,
    ClearMemoryCommand,
    CommandPayload,
)
from .message import (
    AudioSegment,
    FileSegment,
    ImageSegment,
    Segment,
    TextSegment,
    VideoSegment,
)

__all__ = [
    "chat",
    "chat_segments",
    "clear_context",
    "clear_memory",
]


# ── 聊天 ────────────────────────────────────────────────────


def chat(
    bot_id: str,
    session_id: str,
    text: str,
    *,
    role: Role | str = Role.USER,
) -> ChatPayload:
    """快速构建纯文本聊天载荷。

    Args:
        bot_id: Bot 唯一标识。
        session_id: 会话唯一标识。
        text: 消息文本内容。
        role: 发送者角色，默认 ``user``。

    Returns:
        可直接序列化的 ChatPayload。

    Example::

        from chat_hub_protocol.client import chat

        payload = chat("bot-001", "sess-abc", "你好！")
        print(payload.model_dump_json(indent=2))
    """
    return ChatPayload(
        bot_id=bot_id,
        session_id=session_id,
        message=Message.text(role, text),
    )


def chat_segments(
    bot_id: str,
    session_id: str,
    *segments: Segment,
    role: Role | str = Role.USER,
) -> ChatPayload:
    """构建包含任意消息段的聊天载荷（支持图文混排）。

    Args:
        bot_id: Bot 唯一标识。
        session_id: 会话唯一标识。
        *segments: 一个或多个消息段（TextSegment / ImageSegment / …）。
        role: 发送者角色，默认 ``user``。

    Returns:
        可直接序列化的 ChatPayload。

    Example::

        from chat_hub_protocol.client import chat_segments
        from chat_hub_protocol import TextSegment, ImageSegment

        payload = chat_segments(
            "bot-001", "sess-abc",
            TextSegment(text="看看这张图"),
            ImageSegment(url="https://example.com/cat.jpg"),
        )
    """
    return ChatPayload(
        bot_id=bot_id,
        session_id=session_id,
        message=Message(role=Role(role), content=list(segments)),
    )


# ── 命令 ────────────────────────────────────────────────────


def clear_context(bot_id: str, session_id: str) -> CommandPayload:
    """构建"清除上下文"命令载荷。

    Args:
        bot_id: Bot 唯一标识。
        session_id: 会话唯一标识。

    Returns:
        可直接序列化的 CommandPayload。
    """
    return CommandPayload(
        bot_id=bot_id,
        session_id=session_id,
        command=ClearContextCommand(),
    )


def clear_memory(bot_id: str, session_id: str) -> CommandPayload:
    """构建"清除长期记忆"命令载荷。

    Args:
        bot_id: Bot 唯一标识。
        session_id: 会话唯一标识。

    Returns:
        可直接序列化的 CommandPayload。
    """
    return CommandPayload(
        bot_id=bot_id,
        session_id=session_id,
        command=ClearMemoryCommand(),
    )
