from pyrogram import Client, filters

# Ganti nomor DANA dan ShopeePay sesuai kebutuhanmu
DANA_NUMBER = "081234567890"
SHOPEEPAY_NUMBER = "081298765432"

@Client.on_message(filters.command("getpay", prefixes=".") & filters.me)
async def getpay(client, message):
    text = (
        f"Nomor DANA: {DANA_NUMBER}\n"
        f"Nomor ShopeePay: {SHOPEEPAY_NUMBER}"
    )
    await message.reply_text(text)
