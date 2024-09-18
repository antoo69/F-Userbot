from pyrogram import Client, filters
import qrcode
from io import BytesIO

# Fungsi untuk membuat QR Code
def generate_payment_qrcode(payment_link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(payment_link)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    # Simpan QR code ke dalam buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer

# Handler untuk perintah .getpay
@Client.on_message(filters.command("getpay", prefixes=".") & filters.me)
async def send_payment_qr(client, message):
    # Ganti ini dengan link pembayaran yang valid
    payment_link = "https://docs.google.com/document/d/1kkxTaiZCTFdYMHJfS2emD4uUZFbSTnbG2sbWk6G62Z0/edit?usp=drivesdk"
    
    # Buat QR Code dan dapatkan buffer image-nya
    qr_image = generate_payment_qrcode(payment_link)
    
    # Kirim QR Code ke chat
    await client.send_photo(
        chat_id=message.chat.id,
        photo=qr_image,
        caption="Scan untuk melakukan pembayaran."
    )
