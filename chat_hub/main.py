"""应用入口。"""

from __future__ import annotations

from chat_hub.hub import Hub

hub = Hub()


def main() -> None:
    """启动 Chat Hub 服务。"""
    from chat_hub.config import settings

    print(f"Chat Hub starting on {settings.host}:{settings.port} ...")
    # TODO: 在此处启动实际的服务（如 FastAPI / WebSocket 等）


if __name__ == "__main__":
    main()
