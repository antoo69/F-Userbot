import asyncio
import signal

import tornado.ioloop
import tornado.platform.asyncio
from pyrogram.errors import (AccessTokenExpired, AccessTokenInvalid,
                             ApiIdInvalid, SessionExpired, UserDeactivated)

from beban import (autor_all, autor_bot, autor_ch, autor_gc, autor_mention,
                   autor_us)
from Mix import *
from Mix.core.gclog import check_logger, getFinish
from Mix.core.waktu import auto_clean
from handlers.bot_maker import api_key, start_userbot, aktif_command
from config import BOT_TOKEN

async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def start_user():
    LOGGER.info("Starting Telegram User Client...")
    try:
        await nlx.start()
    except SessionExpired as e:
        LOGGER.info(f"Error {e}")
        sys.exit(1)
    except ApiIdInvalid as e:
        LOGGER.info(f"Error {e}")
        sys.exit(1)
    except UserDeactivated as e:
        LOGGER.info(f"Error {e}")
        sys.exit(1)

async def start_bot():
    LOGGER.info("Starting Telegram Bot Client...")
    if BOT_TOKEN is None:
        await autobot()
    try:
        await bot.start()
    except AccessTokenInvalid as e:
        print(f"Error : {e}")
        ndB.del_key("BOT_TOKEN")
        sys.exit(1)
    except AccessTokenExpired as e:
        print(f"Error : {e}")
        ndB.del_key("BOT_TOKEN")
        sys.exit(1)

async def starter():
    LOGGER.info("Check Updater...")
    await cek_updater()
    LOGGER.info("Updater Finished...")
    LOGGER.info(f"Connecting to {ndB.name}...")
    if ndB.ping():
        LOGGER.info(f"Connected to {ndB.name} Successfully!")
    await start_user()
    if nlx.is_connected:
        await start_bot()
        await check_logger()

async def main():
    await starter()
    await asyncio.gather(refresh_cache(), getFinish())
    LOGGER.info("Successfully Started Userbot.")
    
    # Menjalankan semua tugas autor
    tasks = [
        asyncio.create_task(auto_clean()),
        asyncio.create_task(autor_gc()),
        asyncio.create_task(autor_ch()),
        asyncio.create_task(autor_us()),
        asyncio.create_task(autor_bot()),
        asyncio.create_task(autor_mention()),
        asyncio.create_task(autor_all())
    ]
    
    await asyncio.gather(*tasks, isFinish())
    
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda: asyncio.create_task(shutdown(s, loop)))
    
    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await bot.stop()

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
