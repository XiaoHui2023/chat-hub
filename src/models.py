"""SQLiter 数据模型定义。

定义持久化到 SQLite 的数据表结构，供 SessionScope 使用。
"""

from __future__ import annotations

from sqliter.model import BaseDBModel


class StoredMessage(BaseDBModel):
    """持久化的聊天消息。"""

    bot_id: str
    session_id: str
    role: str
    content: str
    """JSON 序列化的 list[Segment]。"""

    class Meta:
        table_name = "messages"


class StoredMemory(BaseDBModel):
    """持久化的长期记忆（按 bot 维度）。"""

    bot_id: str
    key: str
    value: str
    """JSON 序列化的任意值。"""

    class Meta:
        table_name = "memories"
        unique_together = [("bot_id", "key")]


class SessionConfig(BaseDBModel):
    """会话级配置。"""

    bot_id: str
    session_id: str
    key: str
    value: str
    """JSON 序列化的配置值。"""

    class Meta:
        table_name = "session_configs"
        unique_together = [("bot_id", "session_id", "key")]
