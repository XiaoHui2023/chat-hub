"""chat-hub-protocol 基础测试。"""

from chat_hub_protocol import (
    ChatPayload,
    ImageSegment,
    Message,
    Role,
    TextSegment,
)


def test_text_message_shortcut() -> None:
    msg = Message.text(Role.USER, "hello")
    assert len(msg.content) == 1
    assert isinstance(msg.content[0], TextSegment)
    assert msg.content[0].text == "hello"


def test_mixed_content_message() -> None:
    msg = Message(
        role=Role.USER,
        content=[
            TextSegment(text="看看这张图："),
            ImageSegment(url="https://example.com/cat.png", alt="一只猫"),
        ],
    )
    assert len(msg.content) == 2


def test_chat_payload_serialization() -> None:
    payload = ChatPayload(
        bot_id="bot-001",
        session_id="sess-abc",
        message=Message.text(Role.USER, "你好"),
    )
    data = payload.model_dump()
    assert data["bot_id"] == "bot-001"
    assert data["session_id"] == "sess-abc"

    # 反序列化
    restored = ChatPayload.model_validate(data)
    assert restored.bot_id == payload.bot_id
    assert restored.message.content[0].text == "你好"  # type: ignore[union-attr]


def test_payload_json_round_trip() -> None:
    payload = ChatPayload(
        bot_id="bot-002",
        session_id="sess-xyz",
        message=Message.text(Role.ASSISTANT, "好的"),
    )
    json_str = payload.model_dump_json()
    restored = ChatPayload.model_validate_json(json_str)
    assert restored == payload
