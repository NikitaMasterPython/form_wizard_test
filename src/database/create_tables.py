import sqlite3

from src.configs.db import PATH_TO_DB
from src.configs.log_config import logger

TEMPLATE = """
CREATE TABLE IF NOT EXISTS templates (
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    user_id INTEGER
);

CREATE TABLE IF NOT EXISTS arguments(
    code TEXT NOT NULL,
    description TEXT NOT NULL,
    templates_rowid INTEGER,
    FOREIGN KEY(templates_rowid) REFERENCES templates(rowid)
);
"""


async def create_tables():
    logger.info(f"Creating tables in {PATH_TO_DB}")
    connection = sqlite3.connect(PATH_TO_DB)
    cursor = connection.cursor()
    cursor.executescript(TEMPLATE)
    cursor.close()
    connection.close()
    logger.info("Creating tables completed")
