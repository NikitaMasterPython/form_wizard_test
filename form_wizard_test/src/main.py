import asyncio
import threading

from src.database.create_tables import create_tables
from src.handliers.start import start_router
from src.tg_bot.main import (
    bot,
    dp,
)


class ThreadedEventLoop(threading.Thread):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


async def main():
    dp.include_router(start_router)
    await create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
