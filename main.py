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

kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Проверить подписку", callback_data="check")]
])

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Нажми кнопку ниже, чтобы проверить подписку на канал:",
        reply_markup=kb
    )

@dp.callback_query(F.data == "check")
async def check_sub(callback: types.CallbackQuery):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, callback.from_user.id)

        if member.status in ["member", "administrator", "creator"]:
            await callback.message.answer("Ты подписан на канал. Добро пожаловать!")
        else:
            await callback.message.answer("Ты не подписан. Подпишись и попробуи снова.")
    except:
        await callback.message.answer("Я не могу проверить подписку. Убедись, что ты зашел в канал.")

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
