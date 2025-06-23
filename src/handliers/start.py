from aiogram import (
    F,
    Router,
)
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    t2 = 11111
    t1 = 22222
    await message.answer("Никита создал бота, на шаг ближе к джуну.")


@start_router.message(Command("start_2"))
async def cmd_start_2(message: Message):
    await message.answer("Запуск сообщения по команде /start_2 используя фильтр Command()")


@start_router.message(F.text == "/start_3")
async def cmd_start_3(message: Message):
    await message.answer("Запуск сообщения по команде /start_3 используя магический фильтр F.text!")
