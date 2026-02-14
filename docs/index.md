# Chat Hub

**统一聊天消息路由中心**

Chat Hub 是一个轻量级的聊天消息路由框架，负责将聊天请求分发到不同的 Bot 处理函数，并统一管理会话与消息协议。

## 特性

- **统一协议** — 定义了完整的聊天协议（消息、事件、命令），客户端与服务端共享同一套数据结构
- **多媒体消息** — 支持文本、图片、音频、视频、文件等多种消息类型，天然支持图文混排
- **消息路由** — 通过 `bot_id` 将请求路由到对应的 Bot 处理函数
- **流式响应** — 内置流式事件类型（`STREAM_START` / `STREAM_DELTA` / `STREAM_END`）
- **命令系统** — 支持清除上下文、清除记忆、设置参数等控制命令
- **类型安全** — 基于 Pydantic v2 构建，完整的类型校验与序列化支持

## 项目结构

```
chat-hub/
├── src/                           # 主应用
│   ├── __main__.py                # 应用入口（python -m src）
│   ├── hub.py                     # Hub 路由核心
│   └── config.py                  # 应用配置
├── packages/
│   └── protocol/                  # 协议包（可独立发布）
│       └── chat_hub_protocol/
│           ├── chat.py            # 聊天数据结构
│           ├── message.py         # 消息类型定义
│           └── command.py         # 命令协议定义
└── docs/                          # 文档源文件
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 数据模型 | Pydantic v2 |
| 配置管理 | pydantic-settings |
| Python 版本 | >= 3.11 |
| 构建工具 | Hatchling（协议包） |
| 代码检查 | Ruff |
