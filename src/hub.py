"""Hub 核心：消息路由与 Bot 注册。"""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

from chat_hub_protocol import ChatEvent, ChatPayload

# Bot 处理函数签名
BotHandler = Callable[[ChatPayload], Coroutine[Any, Any, ChatEvent]]


class Hub:
    """管理已注册的 Bot，并将请求路由到对应的处理函数。"""

    def __init__(self) -> None:
        self._handlers: dict[str, BotHandler] = {}

    def register(self, bot_id: str, handler: BotHandler) -> None:
        """注册一个 Bot 处理函数。"""
        if bot_id in self._handlers:
            raise ValueError(f"Bot '{bot_id}' 已注册")
        self._handlers[bot_id] = handler

    def unregister(self, bot_id: str) -> None:
        """注销一个 Bot。"""
        self._handlers.pop(bot_id, None)

    async def dispatch(self, payload: ChatPayload) -> ChatEvent:
        """将聊天载荷分发到对应的 Bot 处理函数。"""
        handler = self._handlers.get(payload.bot_id)
        if handler is None:
            from chat_hub_protocol import EventType

            return ChatEvent(
                event=EventType.ERROR,
                bot_id=payload.bot_id,
                session_id=payload.session_id,
                error=f"未找到 Bot: {payload.bot_id}",
                request_id=payload.request_id,
            )
        return await handler(payload)

    @property
    def bot_ids(self) -> list[str]:
        """返回所有已注册的 Bot ID。"""
        return list(self._handlers.keys())
