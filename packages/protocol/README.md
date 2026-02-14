# chat-hub-protocol

Chat Hub 通信协议包，定义客户端与服务端的公共数据结构。

## 安装

```bash
pip install chat-hub-protocol
```

## 快速使用

```python
from chat_hub_protocol import ChatPayload, Message, Role

# 创建纯文本消息
msg = Message.text(Role.USER, "你好！")

# 构建聊天载荷
payload = ChatPayload(
    bot_id="bot-001",
    session_id="sess-abc",
    message=msg,
)

# 序列化为 JSON
print(payload.model_dump_json(indent=2))
```

## 消息类型

| 类型 | Segment 类 | 说明 |
|------|-----------|------|
| 文本 | `TextSegment` | 纯文本内容 |
| 图片 | `ImageSegment` | 图片 URL / base64 |
| 音频 | `AudioSegment` | 音频文件 |
| 视频 | `VideoSegment` | 视频文件 |
| 文件 | `FileSegment` | 任意文件 |

一条 `Message` 的 `content` 是 `list[Segment]`，天然支持图文混排。
