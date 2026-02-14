"""会话路由组件。

为每个 (bot_id, session_id) 组合提供一个 SessionScope 实例，
通过它访问该会话下的消息、记忆、配置等数据，无需重复传递 ID。

用法::

    session = SessionScope(db, bot_id="bot-001", session_id="sess-abc")

    session.messages.add(role="user", content=[{"type": "text", "text": "你好"}])
    session.messages.list()
    session.messages.clear()

    session.memory.set("user_name", "小明")
    session.memory.get("user_name")

    session.config.set("context_length", 30)
    session.config.get("context_length", default=20)
"""

from __future__ import annotations

import json
from typing import Any

from sqliter import SqliterDB

from src.models import SessionConfig, StoredMemory, StoredMessage


# ── 子访问器 ──────────────────────────────────────────────


class MessageAccessor:
    """会话消息（短期记忆 / 上下文）访问器。"""

    def __init__(self, db: SqliterDB, bot_id: str, session_id: str) -> None:
        self._db = db
        self._bot_id = bot_id
        self._session_id = session_id

    def add(self, role: str, content: list[dict[str, Any]]) -> StoredMessage:
        """添加一条消息。"""
        msg = StoredMessage(
            bot_id=self._bot_id,
            session_id=self._session_id,
            role=role,
            content=json.dumps(content, ensure_ascii=False),
        )
        return self._db.insert(msg)

    def list(self, limit: int | None = None) -> list[dict[str, Any]]:
        """获取消息列表（正序），limit 为取最近 N 条。"""
        query = (
            self._db.select(StoredMessage)
            .filter(bot_id=self._bot_id, session_id=self._session_id)
            .order("pk")
        )
        rows = query.fetch_all()
        if limit is not None and len(rows) > limit:
            rows = rows[-limit:]
        return [
            {
                "pk": r.pk,
                "role": r.role,
                "content": json.loads(r.content),
                "created_at": r.created_at,
            }
            for r in rows
        ]

    def clear(self) -> None:
        """清除该会话的所有消息。"""
        self._db.select(StoredMessage).filter(
            bot_id=self._bot_id, session_id=self._session_id
        ).delete()


class MemoryAccessor:
    """长期记忆访问器（按 bot 维度）。"""

    def __init__(self, db: SqliterDB, bot_id: str) -> None:
        self._db = db
        self._bot_id = bot_id

    def get(self, key: str, default: Any = None) -> Any:
        """获取一条记忆。"""
        row = (
            self._db.select(StoredMemory)
            .filter(bot_id=self._bot_id, key=key)
            .fetch_one()
        )
        if row is None:
            return default
        return json.loads(row.value)

    def set(self, key: str, value: Any) -> None:
        """设置一条记忆（已存在则覆盖）。"""
        existing = (
            self._db.select(StoredMemory)
            .filter(bot_id=self._bot_id, key=key)
            .fetch_one()
        )
        if existing is not None:
            existing.value = json.dumps(value, ensure_ascii=False)
            self._db.update(existing)
        else:
            self._db.insert(
                StoredMemory(
                    bot_id=self._bot_id,
                    key=key,
                    value=json.dumps(value, ensure_ascii=False),
                )
            )

    def list_all(self) -> dict[str, Any]:
        """列出该 bot 的所有记忆。"""
        rows = (
            self._db.select(StoredMemory)
            .filter(bot_id=self._bot_id)
            .fetch_all()
        )
        return {r.key: json.loads(r.value) for r in rows}

    def delete(self, key: str) -> None:
        """删除一条记忆。"""
        self._db.select(StoredMemory).filter(
            bot_id=self._bot_id, key=key
        ).delete()

    def clear(self) -> None:
        """清除该 bot 的所有记忆。"""
        self._db.select(StoredMemory).filter(bot_id=self._bot_id).delete()


class ConfigAccessor:
    """会话级配置访问器。"""

    def __init__(self, db: SqliterDB, bot_id: str, session_id: str) -> None:
        self._db = db
        self._bot_id = bot_id
        self._session_id = session_id

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值。"""
        row = (
            self._db.select(SessionConfig)
            .filter(bot_id=self._bot_id, session_id=self._session_id, key=key)
            .fetch_one()
        )
        if row is None:
            return default
        return json.loads(row.value)

    def set(self, key: str, value: Any) -> None:
        """设置配置值（已存在则覆盖）。"""
        existing = (
            self._db.select(SessionConfig)
            .filter(bot_id=self._bot_id, session_id=self._session_id, key=key)
            .fetch_one()
        )
        if existing is not None:
            existing.value = json.dumps(value, ensure_ascii=False)
            self._db.update(existing)
        else:
            self._db.insert(
                SessionConfig(
                    bot_id=self._bot_id,
                    session_id=self._session_id,
                    key=key,
                    value=json.dumps(value, ensure_ascii=False),
                )
            )

    def list_all(self) -> dict[str, Any]:
        """列出该会话的所有配置。"""
        rows = (
            self._db.select(SessionConfig)
            .filter(bot_id=self._bot_id, session_id=self._session_id)
            .fetch_all()
        )
        return {r.key: json.loads(r.value) for r in rows}


# ── 会话路由 ──────────────────────────────────────────────


class SessionScope:
    """会话作用域，绑定 bot_id + session_id，路由到各数据访问器。"""

    def __init__(self, db: SqliterDB, bot_id: str, session_id: str) -> None:
        self.bot_id = bot_id
        self.session_id = session_id
        self._db = db

    @property
    def messages(self) -> MessageAccessor:
        """该会话的消息（短期记忆 / 上下文）。"""
        return MessageAccessor(self._db, self.bot_id, self.session_id)

    @property
    def memory(self) -> MemoryAccessor:
        """该 bot 的长期记忆。"""
        return MemoryAccessor(self._db, self.bot_id)

    @property
    def config(self) -> ConfigAccessor:
        """该会话的配置。"""
        return ConfigAccessor(self._db, self.bot_id, self.session_id)
