from gigachat import GigaChat
from gigachat.models import (
    Chat,
    Messages,
    MessagesRole,
)

from src.configs.config import settings
from src.sevices.templates.get_templates import GetTemplates


class GIGAChatService:
    """Взаимодействие с GIGA чатом"""

    @classmethod
    async def request_function(cls, message: str, user_id: int) -> str:
        """Обращение к модели"""
        with GigaChat(credentials=settings.GIGA_AUTHORIZATION_KEY, verify_ssl_certs=False, model="GigaChat") as giga:
            response = giga.chat(
                Chat(
                    messages=[
                        Messages(
                            role=MessagesRole.USER,
                            content=message,
                        )
                    ],
                    functions=[GetTemplates.GET_ALL_TEMPLATES, GetTemplates.GET_TEMPLATE_VARIABLES],
                )
            )
        if function_name := response.choices[0].message.function_call:
            return await getattr(GetTemplates, function_name.name)(user_id=user_id, user_request=message)
        return response.choices[0].message.content

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
