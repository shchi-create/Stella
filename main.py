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

# Inline-кнопка для проверки подписки
check_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Получить промокод", callback_data="check")]
])

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Нажми кнопку ниже, чтобы получить промокод:",
        reply_markup=check_kb
    )

# Обработчик нажатия Inline-кнопки
@dp.callback_query(F.data == "check")
async def check_subscription(callback: types.CallbackQuery):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, callback.from_user.id)
        if member.status in ["member", "administrator", "creator"]:
            await callback.message.answer("Промокод: FORTUNA26")
        else:
            await callback.message.answer("Сначала нужно подписаться на наш канал")
    except:
        await callback.message.answer("Ошибка")

    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
