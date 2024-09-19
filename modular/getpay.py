from pyrogram import Client, filters

# Ganti nomor DANA dan ShopeePay sesuai kebutuhanmu
DANA_NUMBER = "087873724521 a/n fer*** sya***"
SHOPEEPAY_NUMBER = "+6287873724521 a/n antbar32"

@Client.on_message(filters.command("getpay", prefixes=".") & filters.me)
async def getpay(client, message):
    text = (
        f"DANA: {DANA_NUMBER}\n"
        f"ShopeePay: {SHOPEEPAY_NUMBER}"
    )
    await message.reply_text(text)
