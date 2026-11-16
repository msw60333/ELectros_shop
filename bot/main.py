import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message , ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.fsm.context import FSMContext


from config import BOT_TOKEN
from database.db import init_db
from bot.registration import Registration, router as registration_router
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)  
db = Dispatcher(storage=MemoryStorage())


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton (text="🚀 Начать")]
        ],
        resize_keyboard=True
    )
    return keyboard



@db.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в наш интернет-магазин!\n"
        "Здесь ты сможешь выбирать товары, "
        "добавлять их в корзину и оформлять заказы.\n\n"
        "Нажми кнопку ниже, чтобы начать регистрацию.", reply_markup=start_keyboard()
        )
    


@db.message(F.text == "🚀 Начать")
async def menu_handler(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_name)

    await message.answer(
        "Давай зарегистрируемся!\n\n"
        "Напиши своё имя и фамилию."
    )


async def main():
    init_db()  
    db.include_router(registration_router)
    
    print("Бот запущен. Ожидание сообщений...")
    
    await db.start_polling(bot)

    

if __name__ == "__main__":
    asyncio.run(main())