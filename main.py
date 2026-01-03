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
    [types.InlineKeyboardButton(text="Проверить подписку", callback_data="check")]
])

# Reply-кнопка /start под строкой ввода (отображается один раз)
start_kb = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="/start")]],
    resize_keyboard=True,
    one_time_keyboard=True  # кнопка исчезает после нажатия
)

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: types.Message):
    # Если это первый запуск — покажем кнопку START
    if message.text == "/start":
        await message.answer(
            "Привет! Нажми кнопку ниже, чтобы проверить подписку на канал:",
            reply_markup=start_kb
        )
    # После нажатия кнопки /start показываем Inline-кнопку и убираем Reply-клавиатуру
    await message.answer(
        "Теперь нажми 'Проверить подписку':",
        reply_markup=check_kb
    )
    await message.answer(" ", reply_markup=types.ReplyKeyboardRemove())  # скрываем кнопку START

# Обработчик нажатия Inline-кнопки
@dp.callback_query(F.data == "check")
async def check_subscription(callback: types.CallbackQuery):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, callback.from_user.id)
        if member.status in ["member", "administrator", "creator"]:
            await callback.message.answer("Ты подписан на канал. Добро пожаловать!")
        else:
            await callback.message.answer("Ты не подписан. Подпишись и попробуй снова.")
    except:
        await callback.message.answer("Не могу проверить подписку. Убедись, что ты зашел в канал.")

    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
