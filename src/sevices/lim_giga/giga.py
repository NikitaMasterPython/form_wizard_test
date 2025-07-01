from gigachat import GigaChat
from gigachat.models import (
    Chat,
    Messages,
    MessagesRole,
)

from src.configs.config import settings


class GIGAChatService:
    """Взаимодействие с GIGA чатом"""

    @classmethod
    async def request(cls, message: str) -> str:
        """Обработка набора сообщений в LLM"""
        messages = [
            Messages(
                role=MessagesRole.USER,
                content=message,
            )
        ]
        with GigaChat(credentials=settings.GIGA_AUTHORIZATION_KEY, verify_ssl_certs=False, model="GigaChat") as giga:
            response = giga.chat(Chat(messages=messages))
        return response.choices[0].message.content
