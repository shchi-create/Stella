import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@svetlanafortunatur"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kb = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="START")]],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Нажми кнопку START", reply_markup=kb)

@dp.message(F.text == "START")
async def ask_user(message: types.Message):
    await message.answer("Кого ищем? Напиши @username")

@dp.message(F.text.startswith("@"))
async def check_user(message: types.Message):
    username = message.text.replace("@", "").strip()

    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=username
        )

        if member.status in ["member", "administrator", "creator"]:
            await message.answer("Есть такой пользователь")
        else:
            await message.answer("Нет такого пользователя")

    except:
        await message.answer("Нет такого пользователя")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
