"""应用配置。"""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """通过环境变量或 .env 文件加载配置。"""

    model_config = {"env_prefix": "CHAT_HUB_", "env_file": ".env"}

    host: str = "0.0.0.0"
    port: int = 10200
    debug: bool = False
    data_dir: str = "data"
    """持久化数据存储目录。"""


settings = Settings()
