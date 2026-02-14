"""Chat Hub 应用入口。允许通过 `python -m src` 启动服务。"""

from __future__ import annotations

from src.config import settings
from src.hub import Hub

hub = Hub()


def main() -> None:
    """启动 Chat Hub 服务。"""
    print(f"Chat Hub starting on {settings.host}:{settings.port} ...")
    # TODO: 在此处启动实际的服务（如 FastAPI / WebSocket 等）


if __name__ == "__main__":
    main()
