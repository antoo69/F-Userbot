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
from handlers.bot_maker import start_userbot  # Import bot maker

# Inisialisasi klien bot
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]
    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def start_user():
    print("Starting Telegram User Client...")
    try:
        await nlx.start()  # Pastikan nlx adalah instance klien user yang benar
    except (SessionExpired, ApiIdInvalid, UserDeactivated) as e:
        print(f"Error: {e}")
        sys.exit(1)

async def start_bot():
    print("Starting Telegram Bot Client...")
    try:
        await bot.start()
    except (AccessTokenInvalid, AccessTokenExpired) as e:
        print(f"Error: {e}")
        sys.exit(1)

async def starter():
    print("Check Updater...")
    await cek_updater()  # Pastikan ini ada dalam Mix
    print("Updater Finished...")
    print(f"Connecting to database...")
    if ndB.ping():
        print(f"Connected to database successfully!")
    await start_user()  # Start user client
    await start_bot()   # Start bot client
    await check_logger()  # Check logger

async def main():
    await starter()
    await asyncio.gather(refresh_cache(), getFinish())
    print("Successfully Started Userbot.")
    
    task_afk = asyncio.create_task(auto_clean())
    task_gc = asyncio.create_task(autor_gc())
    task_ch = asyncio.create_task(autor_ch())
    task_us = asyncio.create_task(autor_us())
    task_bot = asyncio.create_task(autor_bot())
    task_tag = asyncio.create_task(autor_mention())
    task_all = asyncio.create_task(autor_all())
    
    await asyncio.gather(
        task_afk,
        task_tag,
        task_gc,
        task_ch,
        task_us,
        task_bot,
        task_all,
        isFinish(),
    )

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await bot.stop()
        await nlx.stop()  # Hentikan klien user jika diperlukan

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
