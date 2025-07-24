import sqlite3

from src.configs.db import PATH_TO_DB
from src.configs.log_config import logger
from src.schems.functions import Function


async def add_template(template: Function, user_id):
    """Добавляем шаблон в базу данных"""
    logger.info(f"Insert {template.name}")
    conn = sqlite3.connect(PATH_TO_DB)
    cursor = conn.cursor()
    res = cursor.execute(
        """INSERT INTO templates VALUES (?, ?, ?) RETURNING rowid""",
        (template.description, template.file_path, user_id),
    )
    template_id = res.fetchone()[0]
    for param_name, argument in template.parameters.properties.items():
        cursor.execute(
            """INSERT INTO arguments
               VALUES (?, ?, ?)""",
            (param_name, argument.description, template_id),
        )
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Insert completed")
