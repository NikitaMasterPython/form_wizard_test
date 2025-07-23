import copy
import logging
from sqlite3 import (
    Connection,
    Cursor,
)

from docx.document import Document as DocumentObject
from gigachat import GigaChat
from gigachat.models import (
    Chat,
    Function,
    FunctionParameters,
    Messages,
    MessagesRole,
)
from gigachat.models.function_parameters_property import FunctionParametersProperty

from src.configs.config import settings
from src.configs.db import connection
from src.sevices.templates.create_templates import CreateDocuments

logger = logging.getLogger(__name__)


class GetTemplates:
    """Взаимодействие с шаблонами"""

    GET_ALL_TEMPLATES = Function(
        name="get_all_templates",
        description="Возвращает список сохраненных(загруженных) шаблонов для конкретного пользователя",
        parameters=FunctionParameters(
            properties={
                "limit": FunctionParametersProperty(type="string", description="Количество шаблонов для отображения")
            }
        ),
    )

    GET_TEMPLATE_VARIABLES = Function(
        name="get_template_vars_in_agent",
        description="Возвращает список переменных которые необходимы для заполнения шаблона",
        parameters=FunctionParameters(
            properties={
                "limit": FunctionParametersProperty(type="string", description="Количество шаблонов для отображения")
            }
        ),
    )

    GENERATE_DOCUMENT_FROM_TEMPLATE = Function(
        name="generate_document_from_template",
        description="Вызывай эту функцию когда пользователь просит сделать какой-то документ или заполнить шаблон",
        parameters=FunctionParameters(
            properties={},
            required=[],
        ),
    )

    @classmethod
    @connection
    async def generate_document_from_template(
        cls, user_id: int, user_request: str, conn: Connection = None, cursor: Cursor = None
    ) -> str | DocumentObject:
        """Обработка шаблона заявления на автомобиль"""
        variables = await cls.get_template_vars_in_agent(user_id, user_request, as_list=True)
        if isinstance(variables, str):
            return variables





        template_rowid = variables["template_rowid"]
        foo = copy.deepcopy(cls.GENERATE_DOCUMENT_FROM_TEMPLATE)
        for var in variables["variables"]:
            foo.parameters.properties[var["code"]] = FunctionParametersProperty(
                type="string", description=var["description"]
            )
        with GigaChat(
            credentials=settings.GIGA_AUTHORIZATION_KEY, verify_ssl_certs=False, model="GigaChat-Pro"
        ) as giga:
            response = giga.chat(
                Chat(
                    messages=[Messages(role=MessagesRole.USER, content=user_request)],
                    functions=[foo],
                )
            )
            if function_name := response.choices[0].message.function_call:
                args = function_name.arguments
            else:
                args = {}

            logger.debug(f"Аргументы для шаблона: {args}")  # больше логов
            try:
                cursor.execute("SELECT path FROM templates WHERE ROWID = ?", (template_rowid,))
                path = cursor.fetchone()
                if not path:
                    return "Шаблон не найден"

                create = CreateDocuments(path[0], **args)
                return create.create_doc()

            except Exception as e:
                return f"Ошибка: {str(e)}"

    @classmethod
    @connection
    async def get_all_templates(
        cls, user_id: int, user_request: str, conn: Connection = None, cursor: Cursor = None, as_list: bool = False
    ) -> str | list[dict[str, str]]:
        """Получение списка всех шаблонов"""
        res = cursor.execute(
            "SELECT name, ROWID FROM templates WHERE templates.user_id = ? ORDER BY name", (user_id,)
        ).fetchall()
        if as_list:
            return "\n".join([f"Название шаблона: '{i[0]}', ROWID: {i[1]}" for i in res])
        return "\n".join((f"{num + 1}. {i[0]}" for num, i in enumerate(res)))

    @classmethod
    async def get_template_variables(
        cls, template_rowid: int, conn: Connection = None, cursor: Cursor = None, as_list: bool = False
    ) -> str | dict[str, str | int | list[dict[str, str]]]:
        """Получение всех переменных необходимых для формирования документа"""
        res = cursor.execute(
            "SELECT description, code FROM arguments WHERE templates_rowid = ? ORDER BY description", (template_rowid,)
        ).fetchall()
        if as_list:
            return {"template_rowid": template_rowid, "variables": [{"description": i[0], "code": i[1]} for i in res]}
        return "\n".join((f"{num + 1}. {i[0]}" for num, i in enumerate(res)))

    @classmethod
    @connection
    async def get_template_vars_in_agent(
        cls,
        user_id: int,
        user_request: str,
        conn: Connection = None,
        cursor: Cursor = None,
        as_list: bool = False,
    ):
        """Получение переменных шаблона через, ИИ агента"""
        all_templates = await cls.get_all_templates(user_id, user_request, conn=conn, cursor=cursor, as_list=True)
        all_templates = Messages(
            role=MessagesRole.USER,
            content=all_templates,
        )
        user_request = Messages(
            role=MessagesRole.USER,
            content=user_request,
        )
        command = Messages(
            role=MessagesRole.USER,
            content="Выбери из списка наиболее подходящий шаблон. "
            "Не придумывай переменные просто ответь какое значение ROWID использовать. Ответ верни одной цифрой."
            "Если не один шаблон не подходит верни сообщение: 'У вас нет не одного подходящего шаблона, или я Вас не понял, напишите мне слово Шаблоны, я выведу список, повторите тоже самое, указав номер шаблона, спасибо.'",
        )
        with GigaChat(
            credentials=settings.GIGA_AUTHORIZATION_KEY, verify_ssl_certs=False, model="GigaChat-Pro"
        ) as giga:
            response = giga.chat(Chat(messages=[all_templates, user_request, command]))
        if response.choices[0].message.content.isdigit():
            return await cls.get_template_variables(
                int(response.choices[0].message.content), conn, cursor, as_list=as_list
            )
        return response.choices[0].message.content
