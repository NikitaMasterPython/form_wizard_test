import io

from aiogram import (
    F,
    Router,
    types,
)
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.types import (
    BufferedInputFile,
    Message,
)
from docx.document import Document as DocumentObject

from src.sevices.audio_converter.voice_to_text import VoiceToTextService
from src.sevices.lim_giga.giga import GIGAChatService
from src.sevices.templates.initial_template_preparation import InitialTemplatePreparation

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Никита молодец.")


@start_router.message(Command("start_2"))
async def cmd_start_2(message: Message):
    await message.answer("1.Для подготовки документов обратитесь к боту с запросом «Шаблоны». \n \n "
                         "2. Выберете подходящий шаблон и отправьте соответствующее голосовое "
                         "или текстовое сообщение. \n"
                         "Например, при необходимости подготовки заявления на служебный автомобиль "
                         "запрос должен содержать следующий текст: \n \n "
                         "Подготовь заявление на служебный автомобиль на 20.09.2025 на "
                         "Иванова Ивана Ивановича. \n \n "
                         "Подготовь заявление на оплату расходов к месту проведения отдыха "
                         "на 15000 рублей на Петрова Петра Николаевича \n \n "
                         "Подготовь заявление на офисную бумагу в отдел кадров "
                         "от Петрова Петра Петровича. \n \n"
                         "Подготовь документальное уведомление, 20.03.2025 на территории "
                         "организации запланированы ремонтные работы \n \n "
                         "Подготовь служебную записку на доставку бетомешалка-200 по адресу: "
                         "г. Хабаровск, ул. Пионерская, д.20 от И.И. Иванова \n \n "
                         "Подготовь служебную записку на списание пылесос-А500, "
                         "Иванов Иван Иванович \n \n "
                         "Также вы можете добавлять свои шаблоны.")


@start_router.message(F.text == "/start_3")
async def cmd_start_3(message: Message):
    await message.answer("Запуск сообщения по команде /start_3 используя магический фильтр F.text!")


@start_router.message(F.voice)
async def get_audio_messages(message: Message):
    """Обработка голосовых сообщений"""
    message_text = await VoiceToTextService.parce_voice_message(message)
    answer_llm = await GIGAChatService.request_function(message_text, message.from_user.id)
    if isinstance(answer_llm, str):
        await message.answer(answer_llm)
    elif isinstance(answer_llm, DocumentObject):
        bytes_doc = io.BytesIO()
        answer_llm.save(bytes_doc)
        new_file = BufferedInputFile(bytes_doc.getvalue(), "new_file.docx")
        await message.reply_document(new_file)


@start_router.message(F.document)
async def get_docx_messages(message: Message):
    if message.content_type == types.ContentType.DOCUMENT:
        message_text = await InitialTemplatePreparation.parce_document(message)
        await message.answer(message_text)


@start_router.message()
async def get_all_messages(message: Message):
    """Обработка всех непонятных текстовых сообщений"""
    if message.content_type == types.ContentType.TEXT:
        answer_llm = await GIGAChatService.request_function(message.text, message.from_user.id)
        if isinstance(answer_llm, str):
            await message.answer(answer_llm)
        elif isinstance(answer_llm, DocumentObject):
            bytes_doc = io.BytesIO()
            answer_llm.save(bytes_doc)
            new_file = BufferedInputFile(bytes_doc.getvalue(), "new_file.docx")
            await message.reply_document(new_file)
