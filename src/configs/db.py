import os
import sqlite3
from pathlib import Path

PATH_TO_DB = os.path.join(Path(__file__).absolute().parents[2], Path("data/db.db"))
PATH_TO_FILES = os.path.join(Path(__file__).absolute().parents[2], Path("data/files"))


def connection(func):
    async def wrapper(*args, **kwargs):
        if "conn" not in kwargs:
            conn = sqlite3.connect(PATH_TO_DB)
            cursor = conn.cursor()
            result = await func(*args, conn=conn, cursor=cursor, **kwargs)
            conn.close()
            return result
        else:
            return await func(*args, **kwargs)

    return wrapper
