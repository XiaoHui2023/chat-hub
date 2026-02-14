"""命令协议定义。

定义客户端向服务端发送的控制命令，如清除上下文、清除记忆、设置参数等。
使用 discriminated union 实现类型安全的多态序列化/反序列化。
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, Union
from uuid import uuid4

from pydantic import BaseModel, Field


# ── 具体命令 ──────────────────────────────────────────────


class ClearContextCommand(BaseModel):
    """清除短期记忆（当前会话上下文）。"""

    type: Literal["clear_context"] = "clear_context"


class ClearMemoryCommand(BaseModel):
    """清除长期记忆。"""

    type: Literal["clear_memory"] = "clear_memory"


# ── 联合类型 ──────────────────────────────────────────────

Command = Annotated[
    Union[ClearContextCommand, ClearMemoryCommand],
    Field(discriminator="type"),
]
"""命令联合类型，通过 `type` 字段自动区分具体命令。"""


# ── 请求载荷与响应 ────────────────────────────────────────


class CommandPayload(BaseModel):
    """命令请求载荷。"""

    bot_id: str
    """Bot 唯一标识。"""
    session_id: str
    """会话唯一标识。"""
    command: Command
    """要执行的命令。"""
    request_id: str = Field(default_factory=lambda: uuid4().hex)
    """请求唯一标识，用于链路追踪。"""


class CommandResult(BaseModel):
    """命令执行结果。"""

    bot_id: str
    session_id: str
    command_type: str
    """回显命令类型。"""
    success: bool
    """是否执行成功。"""
    data: dict[str, Any] | None = None
    """命令返回的数据（如当前设置值）。"""
    error: str | None = None
    """失败时的错误信息。"""
    request_id: str | None = None
    """对应请求的唯一标识。"""
