from aiogram import types
from pydantic import BaseModel
from redis.asyncio.client import Redis


class TelegramMessage(BaseModel):
    message_id: int
    chat_id: int


class TelegramMessageStorage:
    def __init__(self, redis: Redis):
        self._prefix = "telegram_messages"
        self._redis = redis

    async def get_last_message(self, user_tg_id: int) -> TelegramMessage | None:
        key = self._create_key(user_tg_id)
        if message_data := await self._get(key):
            return self._deserialize_message(message_data)
        return None

    async def set_last_message(self, message: types.Message) -> None:
        key = self._create_key(message.chat.id)
        message = TelegramMessage(message_id=message.message_id, chat_id=message.chat.id)
        message_data = self._serialize_message(message)
        await self._redis.set(key, message_data)

    def _create_key(self, chat_id: int) -> str:
        return f"{self._prefix}:{chat_id}"

    @staticmethod
    def _serialize_message(message: TelegramMessage) -> str:
        return message.model_dump_json()

    @staticmethod
    def _deserialize_message(message_data: str) -> TelegramMessage:
        return TelegramMessage.model_validate_json(message_data)

    async def _get(self, key: str, encoding: str = "utf-8") -> str | None:
        value = await self._redis.get(key)
        return value.decode(encoding) if value else None
