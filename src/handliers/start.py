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

    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    FSInputFile
)

from aiogram.enums import ParseMode

from docx.document import Document as DocumentObject

from src.sevices.audio_converter.voice_to_text import VoiceToTextService
from src.sevices.lim_giga.giga import GIGAChatService
from src.sevices.templates.initial_template_preparation import InitialTemplatePreparation

from pathlib import Path

TEMPLATES_DIR = Path("templates")  # Папка с шаблонами документов

start_router = Router()

# Создаем клавиатуру с кнопками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Инструкция по использованию"),
            KeyboardButton(text="📄 Шаблоны документов")
        ],
        [
            KeyboardButton(text="❓ Помощь"),
            KeyboardButton(text="⚙️ Добавить шаблон")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие..."
)



@start_router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Добро пожаловать в бота для работы с документами!\n\n"
        "Вы можете использовать кнопки ниже для навигации:\n"
        "- 📋 Инструкция - как работать с ботом\n"
        "- 📄 Шаблоны - список доступных шаблонов\n"
        "- ❓ Помощь - справочная информация\n"
        "- ⚙️ Добавить шаблон - создать свой шаблон"
    )
    await message.answer(welcome_text, reply_markup=main_keyboard)



@start_router.message(F.text == "📋 Инструкция по использованию")
async def show_instructions(message: Message):
    instructions = (
        "1. Для подготовки документов нажмите кнопку «📄 Шаблоны документов».\n"
        "Вам будут направлены имеющиеся шаблоны в формате .docx.\n"
        "Перешлите мне указанные шаблоны для внесения в базу данных.\n\n"
        "2. Выберите подходящий шаблон и отправьте соответствующее голосовое "
        "или текстовое сообщение.\n\n"
        "Примеры запросов:\n"
        "• Подготовь заявление на служебный автомобиль на 20.09.2025 на "
        "Иванова Ивана Ивановича\n"
        "• Подготовь заявление на оплату расходов к месту проведения отдыха "
        "на 15000 рублей на Петрова Петра Николаевича\n"
        "• Подготовь заявление на офисную бумагу в отдел кадров "
        "от Петрова Петра Петровича\n"
        "• Подготовь документальное уведомление, 20.03.2025 на территории "
        "организации запланированы ремонтные работы\n"
        "• Подготовь служебную записку на доставку бетомешалка-200 по адресу: "
        "г. Хабаровск, ул. Пионерская, д.20 от И.И. Иванова\n"
        "• Подготовь служебную записку на списание пылесос-А500, "
        "Иванов Иван Иванович\n\n"
        "3. Вы также можете добавлять свои шаблоны через меню «⚙️ Добавить шаблон»"
    )
    await message.answer(instructions)


@start_router.message(F.text == "📄 Шаблоны документов")
async def show_templates(message: Message):
    # Список доступных шаблонов
    templates = [
        "Коммерческое предложение на выгодных условиях.docx",
        "Заявление на служебный автомобиль.docx",
        "Заявление на оплату расходов к месту проведения отдыха.docx",
        "Заявление на офисную бумагу.docx",
        "Документальное уведомление.docx",
        "Служебная записка на доставку.docx",
        "Служебная записка на списание.docx"

    ]

    # Отправляем сообщение с инструкцией
    await message.answer(
        "Доступные шаблоны документов:\n\n"
        "1. Заявление на служебный автомобиль\n"
        "2. Заявление на оплату расходов\n"
        "3. Заявление на офисную бумагу\n"
        "4. Документальное уведомление\n"
        "5. Служебная записка на доставку\n"
        "6. Служебная записка на списание\n"
        "7. Коммерческое предложение на выгодных условиях\n\n"
        "Сейчас я отправлю вам все шаблоны. "
        "Вы можете переслать нужные мне для добавления в базу данных.",
        reply_markup=ReplyKeyboardRemove()
    )

    # Отправляем все шаблоны пользователю
    for template in templates:
        template_path = TEMPLATES_DIR / template
        if template_path.exists():
            doc = FSInputFile(template_path)
            await message.answer_document(doc, caption=f"Шаблон: {template}")
        else:
            await message.answer(f"Шаблон {template} не найден")

    await message.answer(
        "Перешлите мне документы, которые хотите добавить в базу данных шаблонов.",
        reply_markup=main_keyboard
    )


@start_router.message(F.text == "❓ Помощь")
async def show_help(message: Message):
    help_text = (
        "Если у вас возникли проблемы:\n\n"
        "1. Убедитесь, что ваш запрос соответствует примеру из инструкции\n"
        "2. Для голосовых сообщений говорите четко и разборчиво\n"
        "3. При отправке документов убедитесь, что они в формате DOCX\n\n"
        "По всем вопросам обращайтесь к администратору."
    )
    await message.answer(help_text)


@start_router.message(F.text == "⚙️ Добавить шаблон")
async def add_template(message: Message):
    await message.answer(
        "Чтобы добавить свой шаблон:\n\n"
        "1. Подготовьте документ в формате DOCX в соответствии образцами.\n"
        "При подготовке своего шаблона особое внимание уделить параметрам {{}},"
        "которые нужно заменять.\n"
        "2. Отправьте его этому боту\n\n"
        "Пример:\n"
        "Прошу предоставить {{date}} служебный автомобиль для совершения"
        "поездки в командировку. {{full_name}}.\n"
        "На второй странице документа необходимо указать параметры:\n"
        "<<Заявление на служебный автомобиль>> - название документа.\n "
        "{{date}} - дата когда необходимо воспользоваться автомобилем в формате ДД.ММ.ГГГГ.\n "
        "{{full_name}} - фамилия имя отчество заявителя.",

        reply_markup=ReplyKeyboardRemove(),
        parse_mode=None
    )
    await message.answer(
        "Теперь вы можете отправить мне ваш шаблон документа в формате DOCX:",
        reply_markup=main_keyboard  # Возвращаем основную клавиатуру
    )


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
