# chat-hub-protocol

Chat Hub 通信协议包，定义客户端与服务端的公共数据结构。

## 安装

```bash
pip install chat-hub-protocol
```

从源码安装（开发模式）：

```bash
cd packages/protocol
pip install -e .
```

---

## 快速开始

### 使用 client 便捷函数（推荐）

```python
from chat_hub_protocol import chat, clear_context

# 一行代码构建聊天请求
payload = chat("bot-001", "sess-abc", "你好！")
print(payload.model_dump_json(indent=2))

# 一行代码构建命令请求
cmd = clear_context("bot-001", "sess-abc")
print(cmd.model_dump_json(indent=2))
```

### 手动构建载荷

```python
from chat_hub_protocol import ChatPayload, Message, Role

msg = Message.text(Role.USER, "你好！")

payload = ChatPayload(
    bot_id="bot-001",
    session_id="sess-abc",
    message=msg,
)

print(payload.model_dump_json(indent=2))
```

---

## 客户端便捷函数

所有函数返回 Pydantic 模型，可直接 `.model_dump_json()` 序列化。

### `chat(bot_id, session_id, text, *, role="user")`

快速构建纯文本聊天载荷，返回 `ChatPayload`。

```python
from chat_hub_protocol import chat

payload = chat("bot-001", "sess-abc", "你好！")
```

### `chat_segments(bot_id, session_id, *segments, role="user")`

构建包含任意消息段的聊天载荷，支持图文混排，返回 `ChatPayload`。

```python
from chat_hub_protocol import chat_segments, TextSegment, ImageSegment

payload = chat_segments(
    "bot-001", "sess-abc",
    TextSegment(text="看看这张图"),
    ImageSegment(url="https://example.com/cat.jpg"),
)
```

### `clear_context(bot_id, session_id)`

构建"清除上下文"命令载荷，返回 `CommandPayload`。

```python
from chat_hub_protocol import clear_context

cmd = clear_context("bot-001", "sess-abc")
```

### `clear_memory(bot_id, session_id)`

构建"清除长期记忆"命令载荷，返回 `CommandPayload`。

```python
from chat_hub_protocol import clear_memory

cmd = clear_memory("bot-001", "sess-abc")
```

---

## 消息类型

一条 `Message` 的 `content` 是 `list[Segment]`，天然支持图文混排。

| 类型 | Segment 类 | 说明 |
|------|-----------|------|
| 文本 | `TextSegment` | 纯文本内容 |
| 图片 | `ImageSegment` | 图片 URL / base64，可选 `alt`、`width`、`height` |
| 音频 | `AudioSegment` | 音频地址，可选 `duration` |
| 视频 | `VideoSegment` | 视频地址，可选 `duration`、`cover` |
| 文件 | `FileSegment` | 文件下载地址，必填 `filename`，可选 `size` |

通过 **discriminated union**（`type` 字段）实现类型安全的多态序列化/反序列化。

---

## 聊天协议

### ChatPayload — 聊天请求载荷

| 字段 | 类型 | 说明 |
|------|------|------|
| `bot_id` | `str` | Bot 唯一标识 |
| `session_id` | `str` | 会话唯一标识 |
| `message` | `Message` | 本次携带的消息 |
| `request_id` | `str` | 请求唯一标识（自动生成） |

### ChatEvent — 服务端事件

| 字段 | 类型 | 说明 |
|------|------|------|
| `event` | `EventType` | 事件类型 |
| `bot_id` | `str` | Bot 唯一标识 |
| `session_id` | `str` | 会话唯一标识 |
| `message` | `Message \| None` | 完整消息（MESSAGE / STREAM_END 时携带） |
| `delta` | `str \| None` | 增量文本（STREAM_DELTA 时携带） |
| `error` | `str \| None` | 错误信息（ERROR 时携带） |
| `request_id` | `str \| None` | 对应请求的唯一标识 |

### EventType — 事件类型枚举

| 值 | 说明 |
|----|------|
| `MESSAGE` | 普通完整消息响应 |
| `STREAM_START` | 流式响应开始 |
| `STREAM_DELTA` | 流式响应增量文本 |
| `STREAM_END` | 流式响应结束，携带完整消息 |
| `ERROR` | 错误事件 |

---

## 命令协议

### 命令类型

| 命令类 | `type` 值 | 说明 |
|--------|----------|------|
| `ClearContextCommand` | `clear_context` | 清除当前会话上下文（短期记忆） |
| `ClearMemoryCommand` | `clear_memory` | 清除长期记忆 |

### CommandPayload — 命令请求载荷

| 字段 | 类型 | 说明 |
|------|------|------|
| `bot_id` | `str` | Bot 唯一标识 |
| `session_id` | `str` | 会话唯一标识 |
| `command` | `Command` | 要执行的命令 |
| `request_id` | `str` | 请求唯一标识（自动生成） |

### CommandResult — 命令执行结果

| 字段 | 类型 | 说明 |
|------|------|------|
| `bot_id` | `str` | Bot 唯一标识 |
| `session_id` | `str` | 会话唯一标识 |
| `command_type` | `str` | 回显命令类型 |
| `success` | `bool` | 是否执行成功 |
| `data` | `dict \| None` | 命令返回的数据 |
| `error` | `str \| None` | 失败时的错误信息 |
| `request_id` | `str \| None` | 对应请求的唯一标识 |

---

## 模块结构

```
chat_hub_protocol/
├── __init__.py     # 统一导出
├── chat.py         # Role, Message, ChatPayload, EventType, ChatEvent
├── message.py      # TextSegment, ImageSegment, AudioSegment, VideoSegment, FileSegment
├── command.py      # ClearContextCommand, ClearMemoryCommand, CommandPayload, CommandResult
└── client.py       # 客户端便捷函数：chat, chat_segments, clear_context, clear_memory
```

## 完整文档

查看 [Chat Hub 在线文档](https://XiaoHui2023.github.io/chat-hub/) 获取完整 API 参考与架构说明。
