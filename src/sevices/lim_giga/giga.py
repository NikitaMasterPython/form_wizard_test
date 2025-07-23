import logging

from gigachat import GigaChat
from gigachat.models import (
    Chat,
    Messages,
    MessagesRole,
)

from src.configs.config import settings
from src.sevices.templates.get_templates import GetTemplates

logger = logging.getLogger(__name__)


class GIGAChatService:
    """Взаимодействие с GIGA чатом"""

    @classmethod
    async def request_function(cls, message: str, user_id: int) -> str:
        """Обращение к модели с обработкой шаблонов"""
        messages = [
            Messages(
                role=MessagesRole.SYSTEM,
                content="Ты помогаешь заполнять шаблоны заявлений. Извлекай точные данные из запроса.",
            ),
            Messages(role=MessagesRole.USER, content=message),
        ]

        with GigaChat(
            credentials=settings.GIGA_AUTHORIZATION_KEY, verify_ssl_certs=False, model="GigaChat-Pro"
        ) as giga:
            response = giga.chat(
                Chat(
                    messages=messages,
                    functions=[
                        GetTemplates.GET_ALL_TEMPLATES,
                        GetTemplates.GET_TEMPLATE_VARIABLES,
                        GetTemplates.GENERATE_DOCUMENT_FROM_TEMPLATE,
                    ],
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
