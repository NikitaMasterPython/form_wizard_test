from aiogram.types import Message

from src.configs.log_config import logger
from src.sevices.audio_converter.converter import Converter
from src.sevices.files import FilesService


class VoiceToTextService:
    """Сервис для работы с голосовыми сообщениями"""

    @classmethod
    async def parce_voice_message(cls, message: Message) -> str:
        """Преобразование голосового сообщения в текст"""
        downloaded_file = await FilesService.get_file(message.voice.file_id)
        file_name = f"{message.message_id}.ogg"
        name = message.chat.first_name if message.chat.first_name else "No_name"
        logger.info(f"Chat {name} (ID: {message.chat.id}) download file {file_name}")

        with open(file_name, "wb") as new_file:
            new_file.write(downloaded_file.read())

        converter = Converter(file_name)
        message_text = converter.audio_to_text()
        del converter
        return message_text
