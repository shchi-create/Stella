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

# Inline-кнопка "Проверить подписку"
check_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Проверить подписку", callback_data="check")]
])

# Кнопки для пользователей, которые ещё не подписаны
subscribe_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/svetlanafortunatur")],
    [types.InlineKeyboardButton(text="Проверить снова", callback_data="check")]
])

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы проверить подписку на канал:",
        reply_markup=check_kb
    )

# Обработчик нажатия Inline-кнопки
@dp.callback_query(F.data == "check")
async def check_subscription(callback: types.CallbackQuery):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, callback.from_user.id)

        if member.status in ["member", "administrator", "creator"]:
            await callback.message.answer("Ты подписан на канал. Добро пожаловать!")
        else:
            await callback.message.answer(
                "Ты ещё не подписан на канал. Подпишись, а затем нажми кнопку ниже, чтобы проверить снова:",
                reply_markup=subscribe_kb
            )
    except:
        await callback.message.answer(
            "Не могу проверить подписку. Убедись, что ты зашел в канал и нажми кнопку снова:",
            reply_markup=subscribe_kb
        )

    # Обязательный ответ на callback_query
    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
