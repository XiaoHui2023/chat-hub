# 架构概览

## 整体架构

Chat Hub 采用**单体仓库（monorepo）** 结构，包含两个主要部分：

```
┌─────────────────────────────────────────────┐
│                  客户端                       │
│         (使用 chat-hub-protocol)             │
└────────────────┬────────────────────────────┘
                 │  ChatPayload / CommandPayload
                 ▼
┌─────────────────────────────────────────────┐
│              Chat Hub 服务                    │
│  ┌─────────────────────────────────────┐    │
│  │              Hub 路由               │    │
│  │  • 注册/注销 Bot                    │    │
│  │  • 根据 bot_id 分发请求            │    │
│  └──────┬──────────┬──────────┬───────┘    │
│         │          │          │             │
│    ┌────▼───┐ ┌────▼───┐ ┌───▼────┐       │
│    │ Bot A  │ │ Bot B  │ │ Bot C  │       │
│    └────┬───┘ └────┬───┘ └───┬────┘       │
│         │          │          │             │
└─────────┼──────────┼──────────┼─────────────┘
          │          │          │
          ▼          ▼          ▼
      ChatEvent  ChatEvent  ChatEvent
```

## 核心模块

### 1. 协议层 (`chat_hub_protocol`)

独立可发布的协议包，定义客户端与服务端之间的公共数据结构。

| 模块 | 职责 |
|------|------|
| `chat.py` | 聊天核心类型：`Message`、`ChatPayload`、`ChatEvent`、`Role`、`EventType` |
| `message.py` | 消息内容段：`TextSegment`、`ImageSegment`、`AudioSegment`、`VideoSegment`、`FileSegment` |
| `command.py` | 控制命令：`ClearContextCommand`、`ClearMemoryCommand`、`SetContextLengthCommand` |

### 2. 应用层 (`src`)

| 模块 | 职责 |
|------|------|
| `hub.py` | Hub 核心，管理 Bot 注册和消息路由 |
| `config.py` | 应用配置，通过环境变量/`.env` 加载 |
| `__main__.py` | 应用入口 |

## 数据流

### 聊天流程

```
1. 客户端构建 ChatPayload（包含 bot_id、session_id、message）
2. 发送到 Chat Hub 服务
3. Hub.dispatch() 根据 bot_id 找到对应的 BotHandler
4. BotHandler 处理请求，返回 ChatEvent
5. ChatEvent 推送给客户端
```

### 消息模型

一条消息 (`Message`) 由多个内容段 (`Segment`) 组成：

```
Message
├── role: Role (user / assistant / system)
├── content: list[Segment]
│   ├── TextSegment(type="text", text="你好")
│   ├── ImageSegment(type="image", url="...")
│   └── ...
└── timestamp: datetime
```

通过 **discriminated union**（基于 `type` 字段）实现类型安全的多态序列化。

### 事件类型

| 事件 | 说明 |
|------|------|
| `MESSAGE` | 完整消息响应 |
| `STREAM_START` | 流式响应开始 |
| `STREAM_DELTA` | 流式响应增量文本 |
| `STREAM_END` | 流式响应结束，携带完整消息 |
| `ERROR` | 错误事件 |
