"""消息内容类型定义。

支持文本、图片、音频、视频、文件等多种消息类型，
使用 discriminated union 实现类型安全的多态序列化/反序列化。
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


class TextSegment(BaseModel):
    """文本消息段。"""

    type: Literal["text"] = "text"
    text: str


class ImageSegment(BaseModel):
    """图片消息段。"""

    type: Literal["image"] = "image"
    url: str
    """图片地址（URL 或 base64 data URI）。"""
    alt: str = ""
    """图片替代文本。"""
    width: int | None = None
    height: int | None = None


class AudioSegment(BaseModel):
    """音频消息段。"""

    type: Literal["audio"] = "audio"
    url: str
    """音频地址。"""
    duration: float | None = None
    """时长（秒）。"""


class VideoSegment(BaseModel):
    """视频消息段。"""

    type: Literal["video"] = "video"
    url: str
    """视频地址。"""
    duration: float | None = None
    """时长（秒）。"""
    cover: str | None = None
    """封面图地址。"""


class FileSegment(BaseModel):
    """文件消息段。"""

    type: Literal["file"] = "file"
    url: str
    """文件下载地址。"""
    filename: str
    """文件名。"""
    size: int | None = None
    """文件大小（字节）。"""


# ── 联合类型 ─────────────────────────────────────────────

Segment = Annotated[
    Union[TextSegment, ImageSegment, AudioSegment, VideoSegment, FileSegment],
    Field(discriminator="type"),
]
"""单个消息段，通过 `type` 字段自动区分具体类型。"""
