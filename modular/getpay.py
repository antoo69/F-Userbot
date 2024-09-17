import qrcode
from pyrogram import Client, filters

# Fungsi untuk membuat QR code berdasarkan data pembayaran
def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_path = "/tmp/payment_qr.png"  # Simpan QR code di folder sementara
    img.save(img_path)
    return img_path

# Handler untuk perintah .getpay
@Client.on_message(filters.command("getpay", prefixes=".") & filters.me)
async def getpay(client, message):
    # Ganti dengan link ke dokumen atau halaman yang berisi semua metode pembayaran
    data_pembayaran = "https://docs.google.com/document/d/1kkxTaiZCTFdYMHJfS2emD4uUZFbSTnbG2sbWk6G62Z0/edit?usp=drivesdk"  # Link ke Google Docs atau halaman web
    
    # Buat QR code berdasarkan data pembayaran
    img_path = generate_qr(data_pembayaran)
    
    # Kirim gambar QR code ke chat sebagai balasan
    await message.reply_photo(photo=img_path, caption="Scan kode QR ini untuk melihat semua metode pembayaran.")
