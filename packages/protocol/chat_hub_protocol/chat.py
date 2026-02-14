"""Chat 核心数据结构。

定义 Message（单条消息）和 ChatPayload（完整聊天载荷），
供客户端与服务端之间传输使用。
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from .message import Segment


class Role(str, Enum):
    """消息角色。"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """单条聊天消息。

    一条消息由多个 Segment 组成，允许图文混排。
    """

    role: Role
    """发送者角色。"""
    content: list[Segment]
    """消息内容段列表，支持图文混排。"""
    timestamp: datetime = Field(default_factory=datetime.now)
    """消息时间戳。"""

    # ── 便捷构造 ─────────────────────────────────────

    @classmethod
    def text(cls, role: Role | str, text: str) -> Message:
        """快捷创建纯文本消息。"""
        from .message import TextSegment

        return cls(role=Role(role), content=[TextSegment(text=text)])


class ChatPayload(BaseModel):
    """一次聊天请求/事件的完整载荷。

    包含 bot 标识、会话标识以及消息内容。
    """

    bot_id: str
    """Bot 唯一标识。"""
    session_id: str
    """会话唯一标识。"""
    message: Message
    """本次携带的消息。"""
    request_id: str = Field(default_factory=lambda: uuid4().hex)
    """请求唯一标识，用于链路追踪。"""


class EventType(str, Enum):
    """事件类型。"""

    MESSAGE = "message"
    """普通消息。"""
    STREAM_START = "stream_start"
    """流式响应开始。"""
    STREAM_DELTA = "stream_delta"
    """流式响应增量。"""
    STREAM_END = "stream_end"
    """流式响应结束。"""
    ERROR = "error"
    """错误。"""


class ChatEvent(BaseModel):
    """服务端推送给客户端的聊天事件。"""

    event: EventType
    """事件类型。"""
    bot_id: str
    session_id: str
    message: Message | None = None
    """完整消息（MESSAGE / STREAM_END 时携带）。"""
    delta: str | None = None
    """增量文本（STREAM_DELTA 时携带）。"""
    error: str | None = None
    """错误信息（ERROR 时携带）。"""
    request_id: str | None = None
    """对应请求的唯一标识。"""
