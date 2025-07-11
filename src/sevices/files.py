from src.tg_bot.main import bot


class FilesService:
    """Сервис для обработки файлов"""

    @classmethod
    async def get_file(cls, file_id: str):
        file_info = await bot.get_file(file_id)
        return await bot.download_file(file_info.file_path)
