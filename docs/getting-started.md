# 快速开始

## 安装

### 安装主项目

```bash
git clone https://github.com/XiaoHui2023/chat-hub.git
cd chat-hub
pip install -e .
```

### 仅安装协议包

如果你只需要使用协议数据结构（例如在客户端项目中），可以单独安装协议包：

```bash
pip install chat-hub-protocol
```

## 基本使用

### 创建消息

```python
from chat_hub_protocol import Message, Role

# 创建纯文本消息
msg = Message.text(Role.USER, "你好！")
```

### 构建聊天载荷

```python
from chat_hub_protocol import ChatPayload, Message, Role

msg = Message.text(Role.USER, "你好！")
payload = ChatPayload(
    bot_id="bot-001",
    session_id="sess-abc",
    message=msg,
)

# 序列化为 JSON
print(payload.model_dump_json(indent=2))
```

### 多媒体消息（图文混排）

```python
from chat_hub_protocol import Message, Role, TextSegment, ImageSegment

msg = Message(
    role=Role.USER,
    content=[
        TextSegment(text="请看这张图片："),
        ImageSegment(url="https://example.com/photo.jpg", alt="示例图片"),
    ],
)
```

### 注册 Bot 并处理消息

```python
from chat_hub.hub import Hub
from chat_hub_protocol import ChatPayload, ChatEvent, EventType, Message, Role

hub = Hub()

async def my_bot(payload: ChatPayload) -> ChatEvent:
    """一个简单的回声 Bot。"""
    return ChatEvent(
        event=EventType.MESSAGE,
        bot_id=payload.bot_id,
        session_id=payload.session_id,
        message=Message.text(Role.ASSISTANT, f"收到: {payload.message.content}"),
        request_id=payload.request_id,
    )

# 注册 Bot
hub.register("echo-bot", my_bot)

# 分发消息
# response = await hub.dispatch(payload)
```

### 发送命令

```python
from chat_hub_protocol import (
    CommandPayload,
    ClearContextCommand,
    SetContextLengthCommand,
)

# 清除会话上下文
cmd = CommandPayload(
    bot_id="bot-001",
    session_id="sess-abc",
    command=ClearContextCommand(),
)

# 设置上下文长度
cmd = CommandPayload(
    bot_id="bot-001",
    session_id="sess-abc",
    command=SetContextLengthCommand(length=20),
)
```

## 配置

Chat Hub 通过环境变量或 `.env` 文件加载配置，所有配置项均以 `CHAT_HUB_` 为前缀：

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `CHAT_HUB_HOST` | `0.0.0.0` | 监听地址 |
| `CHAT_HUB_PORT` | `8000` | 监听端口 |
| `CHAT_HUB_DEBUG` | `false` | 调试模式 |

```bash
# .env 文件示例
CHAT_HUB_HOST=127.0.0.1
CHAT_HUB_PORT=9000
CHAT_HUB_DEBUG=true
```
