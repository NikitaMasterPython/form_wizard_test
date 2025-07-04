from aiogram import (
    F,
    Router,
    types,
)
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.types import Message

from src.sevices.audio_converter.voice_to_text import VoiceToTextService
from src.sevices.lim_giga.giga import GIGAChatService

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Никита молодец.")


@start_router.message(Command("start_2"))
async def cmd_start_2(message: Message):
    await message.answer("Запуск сообщения по команде /start_2 используя фильтр Command()")


@start_router.message(F.text == "/start_3")
async def cmd_start_3(message: Message):
    await message.answer("Запуск сообщения по команде /start_3 используя магический фильтр F.text!")


@start_router.message(F.voice)
async def get_audio_messages(message: Message):
    """Обработка голосовых сообщений"""
    message_text = await VoiceToTextService.parce_voice_message(message)
    await message.answer(message_text)


@start_router.message()
async def get_all_messages(message: Message):
    """Обработка всех непонятных текстовых сообщений"""
    if message.content_type == types.ContentType.TEXT:
        answer_llm = await GIGAChatService.request(message.text)
        await message.answer(answer_llm)
