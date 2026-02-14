"""FastAPI 接口，对接 chat-hub-protocol。"""

from __future__ import annotations

from fastapi import FastAPI
from sqliter import SqliterDB

from chat_hub_protocol import (
    ChatEvent,
    ChatPayload,
    CommandPayload,
    CommandResult,
    EventType,
    Message,
    Role,
)
from src.config import settings
from src.models import SessionConfig, StoredMemory, StoredMessage
from src.session import SessionScope

# ── 初始化 ────────────────────────────────────────────────

app = FastAPI(title="Chat Hub", version="0.1.0")

db = SqliterDB(f"{settings.data_dir}/chat_hub.db")
db.create_table(StoredMessage)
db.create_table(StoredMemory)
db.create_table(SessionConfig)


def get_session(bot_id: str, session_id: str) -> SessionScope:
    """为指定的 bot_id + session_id 创建会话作用域。"""
    return SessionScope(db, bot_id, session_id)


# ── 消息处理（暂时为空，后续实现）────────────────────────


async def handle_message(session: SessionScope, payload: ChatPayload) -> ChatEvent:
    """处理聊天消息。

    TODO: 在此实现实际的消息处理逻辑（调用 LLM、检索记忆等）。
    """
    # 存储用户消息
    content_dicts = [seg.model_dump() for seg in payload.message.content]
    session.messages.add(role=payload.message.role.value, content=content_dicts)

    # 占位响应
    return ChatEvent(
        event=EventType.MESSAGE,
        bot_id=payload.bot_id,
        session_id=payload.session_id,
        message=Message.text(Role.ASSISTANT, "收到，处理逻辑待实现。"),
        request_id=payload.request_id,
    )


async def handle_command(session: SessionScope, payload: CommandPayload) -> CommandResult:
    """处理控制命令。"""
    command = payload.command
    command_type = command.type

    try:
        match command_type:
            case "clear_context":
                session.messages.clear()
            case "clear_memory":
                session.memory.clear()
            case "set_context_length":
                session.config.set("context_length", command.length)  # type: ignore[union-attr]
            case _:
                return CommandResult(
                    bot_id=payload.bot_id,
                    session_id=payload.session_id,
                    command_type=command_type,
                    success=False,
                    error=f"未知命令: {command_type}",
                    request_id=payload.request_id,
                )
        return CommandResult(
            bot_id=payload.bot_id,
            session_id=payload.session_id,
            command_type=command_type,
            success=True,
            request_id=payload.request_id,
        )
    except Exception as e:
        return CommandResult(
            bot_id=payload.bot_id,
            session_id=payload.session_id,
            command_type=command_type,
            success=False,
            error=str(e),
            request_id=payload.request_id,
        )


# ── 路由 ──────────────────────────────────────────────────


@app.post("/chat", response_model=ChatEvent)
async def chat_endpoint(payload: ChatPayload) -> ChatEvent:
    """聊天接口：接收 ChatPayload，返回 ChatEvent。"""
    session = get_session(payload.bot_id, payload.session_id)
    return await handle_message(session, payload)


@app.post("/command", response_model=CommandResult)
async def command_endpoint(payload: CommandPayload) -> CommandResult:
    """命令接口：接收 CommandPayload，返回 CommandResult。"""
    session = get_session(payload.bot_id, payload.session_id)
    return await handle_command(session, payload)


@app.get("/health")
async def health() -> dict[str, str]:
    """健康检查。"""
    return {"status": "ok"}
