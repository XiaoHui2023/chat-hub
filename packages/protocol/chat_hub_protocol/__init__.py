"""chat-hub-protocol — Chat Hub 通信协议。

独立发布的轻量包，定义客户端与服务端的公共数据结构。
"""

from .chat import ChatEvent, ChatPayload, EventType, Message, Role
from .client import chat, chat_segments, clear_context, clear_memory
from .command import (
    ClearContextCommand,
    ClearMemoryCommand,
    Command,
    CommandPayload,
    CommandResult,
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
    # chat
    "ChatEvent",
    "ChatPayload",
    "EventType",
    "Message",
    "Role",
    # client helpers
    "chat",
    "chat_segments",
    "clear_context",
    "clear_memory",
    # commands
    "ClearContextCommand",
    "ClearMemoryCommand",
    "Command",
    "CommandPayload",
    "CommandResult",
    # message segments
    "AudioSegment",
    "FileSegment",
    "ImageSegment",
    "Segment",
    "TextSegment",
    "VideoSegment",
]
