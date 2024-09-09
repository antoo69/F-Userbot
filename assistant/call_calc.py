from base64 import urlsafe_b64decode
from struct import unpack

from attrify import Attrify as Atr
from pyrogram import *
from pyrogram.enums import *
from pyrogram.helpers import ikb
from pyrogram.types import *

from Mix import *

mmk = {
    "(",
    ")",
    "KLOS",
    "AC",
    "DEL",
    "%",
    "/",
    "*",
    "-",
    "+",
    "00",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ".",
    "=",
}

hitung = []


def calc_help():
    return ikb(
        [
            [
                ("(", "calc_("),
                (")", "calc_)"),
            ],
            [
                ("%", "calc_%"),
                ("AC", "calc_AC"),
                ("DEL", "calc_DEL"),
                ("÷", "calc_/"),
            ],
            [
                ("7", "calc_7"),
                ("8", "calc_8"),
                ("9", "calc_9"),
                ("x", "calc_*"),
            ],
            [
                ("4", "calc_4"),
                ("5", "calc_5"),
                ("6", "calc_6"),
                ("-", "calc_-"),
            ],
            [
                ("1", "calc_1"),
                ("2", "calc_2"),
                ("3", "calc_3"),
                ("+", "calc_+"),
            ],
            [
                ("00", "calc_00"),
                ("0", "calc_0"),
                ("=", "calc_="),
                (".", "calc_."),
            ],
            [
                (cgr("ttup"), "calc_KLOS"),
            ],
        ]
    )


@ky.callback("calc_")
async def _(c, cq):
    global hitung
    kb = calc_help()
    data = cq.data.split("_")[1]
    teks = "Ferdi-Userbot Calculator"
    if data not in mmk:
        return
    user = cq.from_user
    fullname = user.first_name
    if user.last_name:
        fullname += f" {user.last_name}"

    if data == "DEL":
        if hitung:
            hitung = hitung[:-1]
        nan = f"{''.join(hitung)}\n\n{teks}"
        await cq.edit_message_text(
            text=nan,
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
        )
    elif data == "AC":
        hitung = []
        nan = f"{''.join(hitung)}\n\n{teks}"
        await cq.edit_message_text(text=nan, reply_markup=kb, parse_mode=ParseMode.HTML)
    elif data == "=":
        try:
            expression = (
                "".join(hitung).replace("×", "*").replace("÷", "/").replace("^", "**")
            )
            hasil = str(eval(expression))
            await cq.answer(f"Hasil: {hasil}", show_alert=True)
            hitung = [hasil]
            await cq.edit_message_text(text=f"{hasil}\n\n{teks}", reply_markup=kb)
        except Exception as e:
            await cq.answer(f"Error: {str(e)}", show_alert=True)
            hitung = []
    elif data == "KLOS":
        if user.id != nlx.me.id:
            return await cq.answer(
                f"{fullname} KAYA KONTOL! SIRIK AJA LO!\nGAUSAH DIPENCET! ANJING! MEMEK! NGENTOT! BELI SENDIRI SANA!!",
                show_alert=True,
            )
        if cq.message:
            await cq.message.delete()
        elif cq.inline_message_id:
            unPacked = unpacked2(cq.inline_message_id)
            await nlx.delete_messages(unPacked.chat_id, unPacked.message_id)
        hitung = []
        return
    else:
        if user.id != nlx.me.id:
            return await cq.answer(
                f"BELI LAH Ferdi-Userbot WAHAI {fullname}.\nHANYA 35k, ANDA SUDAH BISA MENIKMATI SEKIAN BANYAKNYA FITUR DI Ferdi-Userbot!",
                show_alert=True,
            )
        hitung.append(data)
        nan = f"{''.join(hitung)}\n\n{teks}"
        await cq.edit_message_text(text=nan, reply_markup=kb, parse_mode=ParseMode.HTML)


def unpacked2(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": int(str(chat_id).replace("-", "-100")),
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)


@ky.callback("KLOS")
async def _(_, cq):
    if cq.from_user.id != nlx.me.id:
        return await cq.answer(
            "Hanya pembuat Ferdi-Userbot yang dapat menutup kalkulator.",
            show_alert=True,
        )

    if cq.message:
        await cq.message.delete()
    elif cq.inline_message_id:
        unPacked = unpacked2(cq.inline_message_id)
        await nlx.delete_messages(unPacked.chat_id, unPacked.message_id)
    return
