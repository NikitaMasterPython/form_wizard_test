import io
import os
import re
import uuid
from pathlib import Path
from typing import Optional

import docx
from aiogram.types import (
    Document,
    Message,
)

from src.configs.db import PATH_TO_FILES
from src.configs.log_config import logger
from src.database.add_template import add_template
from src.schems.functions import (
    Argument,
    Function,
    Parameters,
)
from src.sevices.constants import (
    REPLACE_LITERAL,
    SPLIT_LITERAL,
    TEMPLATE_CONSTANT,
    TEMPLATE_TITLE,
)
from src.sevices.files import FilesService


class InitialTemplatePreparation:
    """Сервис для первоначальной обработки шаблонов"""

    @classmethod
    async def parce_document(cls, message: Message) -> str:
        if message.document.file_name.endswith(".docx"):
            function = await cls._docx(message.document)
            await add_template(function, message.from_user.id)
            return f"В БД добавлен шаблон {function.description}"
        return "Файл не соответствует формату. Обрабатываются только файлы docx"

    @classmethod
    async def _docx(cls, document: Document) -> Optional[Function]:
        """Обработка документов типа docx"""
        downloaded_file = await FilesService.get_file(document.file_id)
        file_path = await cls.save_file(downloaded_file, document.file_name)
        document = docx.Document(downloaded_file)
        template_name = None
        template_variables = {}
        for num, i in enumerate(document.paragraphs[-1::-1]):
            text = i.text
            if re.match(TEMPLATE_CONSTANT, text):
                var_data = text.split(SPLIT_LITERAL)
                if len(var_data) > 1:
                    var = var_data[0].strip().split(":")
                    var_name = var[0].replace(REPLACE_LITERAL, "")
                    argument = Argument(type=var[1] if len(var) > 1 else "string", description=" ".join(var_data[1:]))
                    template_variables[var_name] = argument
                    await cls.delete_paragraph(i)
                else:
                    logger.error("".join([num, text, "Не удалось получить данные для формирования переменной."]))
                    continue
            if re.match(TEMPLATE_TITLE, text):
                template_name = text.replace("<<", "").replace(">>", "")
                await cls.delete_paragraph(i)
                break
        parameters = Parameters(properties=template_variables, required=[])
        return Function(description=template_name, parameters=parameters, file_path=file_path)

    @classmethod
    async def delete_paragraph(cls, paragraph) -> None:
        """Удаление параграфа из документа"""
        p = paragraph._element
        p.getparent().remove(p)
        paragraph._p = paragraph._element = None

    @classmethod
    async def save_file(cls, file: io.BytesIO, file_name: str) -> str:
        """Сохранение файла в директории"""
        if Path(os.path.join(PATH_TO_FILES, Path(file_name))).is_file():
            file_name_comp = file_name.split(".")
            file_name_comp[-2] = f"{file_name_comp[-2]}{str(uuid.uuid4())[:4]}"
            file_name = ".".join(file_name_comp)
            return await cls.save_file(file, file_name)

        path = os.path.join(PATH_TO_FILES, Path(file_name))
        with open(path, "wb") as f:
            f.write(file.getvalue())
        return path
