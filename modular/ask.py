import random

import requests
from gpytranslate import Translator

from Mix import *

__modles__ = "TOD"
__help__ = "TOD"

translator = Translator()


async def get_truth(category="classic|kids|party|hot|mixed"):
    try:
        categories = category.split("|")
        random_category = random.choice(categories)
        response = requests.get(
            f"https://api.safone.dev/truth?category={random_category}"
        )
        data = response.json()
        if response.status_code == 200 and "truth" in data:
            truth = await translator.translate(data["truth"], "en", "id")
            return truth
        else:
            return None
    except Exception as e:
        print("Failed to fetch Truth:", e)
        return None


async def get_dare(category="classic|kids|party|hot|mixed"):
    try:
        categories = category.split("|")
        random_category = random.choice(categories)
        response = requests.get(
            f"https://api.safone.dev/dare?category={random_category}"
        )
        data = response.json()
        if response.status_code == 200 and "dare" in data:
            dare = await translator.translate(data["dare"], "en", "id")
            return dare
        else:
            return None
    except Exception as e:
        print("Failed to fetch Dare:", e)
        return None


@ky.ubot("dare", sudo=True)
async def dare_command(client, message):
    proses = await message.reply(f"`Tunggu ...`")
    dare = await get_dare()
    if dare:
        response = f"**Dare:** `{dare}`"
    else:
        response = "**Gagal mengambil Dare. Silakan coba lagi nanti.**"
    await message.reply_text(response)
    await proses.delete()


@ky.ubot("truth", sudo=True)
async def truth_command(client, message):
    proses = await message.reply(f"`Tunggu ...`")
    truth = await get_truth()
    if truth:
        response = f"**Truth :** `{truth}`"
    else:
        response = "**Gagal mengambil Truth. Silakan coba lagi nanti.**"
    await message.reply_text(response)
    await proses.delete()
