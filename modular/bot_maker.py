import os
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pymongo import MongoClient
from config import MONGO_DB, API_ID, API_HASH, ADMIN_IDS

# Inisialisasi MongoDB
mongo_client = MongoClient(MONGO_DB)
db = mongo_client['userbots']

async def start_userbot(client: Client, message):
    user_id = message.from_user.id
    phone_number = message.text.split()[1]  # Mengambil nomor telepon dari perintah

    # Membuat session string
    session_name = f"userbot_{user_id}"
    userbot_client = Client(session_name, api_id=API_ID, api_hash=API_HASH)

    try:
        await userbot_client.start(phone_number)
        session_string = userbot_client.export_session_string()
        
        # Simpan session string dan informasi lainnya ke database
        db.active_users.update_one(
            {"user_id": user_id},
            {"$set": {"session_string": session_string, "phone_number": phone_number}},
            upsert=True
        )
        
        await message.reply(f"Userbot untuk {phone_number} telah dimulai!\nSession String: `{session_string}`")
        
    except SessionPasswordNeeded:
        await message.reply("Anda perlu memasukkan kata sandi dua langkah.")
    except Exception as e:
        await message.reply(f"Terjadi kesalahan: {str(e)}")

@Client.on_message(filters.command("aktif") & filters.user(ADMIN_IDS))
async def aktif_command(client: Client, message):
    if len(message.command) < 2:
        await message.reply("Format yang benar: .aktif <30|1|3|6|12>")
        return
    
    duration = message.command[1]
    if duration not in ["30", "1", "3", "6", "12"]:
        await message.reply("Format yang benar: .aktif <30|1|3|6|12>")
        return
    
    user_id = message.reply_to_message.from_user.id  # Mengambil ID pengguna yang dibalas

    # Simpan durasi aktif di database untuk pengguna tersebut
    db.active_users.update_one(
        {"user_id": user_id},
        {"$set": {"active_days": int(duration)}},
        upsert=True
    )
    await message.reply(f"Userbot untuk pengguna {user_id} aktif selama {duration} hari!")

@Client.on_message(filters.command("deactivate") & filters.user(ADMIN_IDS))
async def deactivate_command(client: Client, message):
    user_id = message.reply_to_message.from_user.id  # Mengambil ID pengguna yang dibalas
    
    # Menghapus durasi aktif dari database
    db.active_users.update_one(
        {"user_id": user_id},
        {"$unset": {"active_days": ""}}
    )
    await message.reply(f"Userbot untuk pengguna {user_id} telah dinonaktifkan.")
