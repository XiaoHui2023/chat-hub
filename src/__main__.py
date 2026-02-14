"""Chat Hub 应用入口。允许通过 `python -m src` 启动服务。"""

from __future__ import annotations

import uvicorn

from models import settings


def main() -> None:
    """启动 Chat Hub 服务。"""
    uvicorn.run(
        "src.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
