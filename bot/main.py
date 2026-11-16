import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message , ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.fsm.context import FSMContext

from bot.keyboards import categories_keyboard
from config import BOT_TOKEN
from database.db import init_db
from database.db import get_db_connection
from bot.registration import Registration, router as registration_router
from bot.keyboards import main_menu_keyboard
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
async def start_handler(message: Message):

    with get_db_connection() as connection:
        user = connection.execute(
            "SELECT name FROM users WHERE telegram_id = ?",
            (message.from_user.id,)
        ).fetchone()

    if user:
        await message.answer(
            f"С возвращением, {user['name']}! 👋\n\n"
            "Рады снова видеть тебя в нашем магазине!",
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.answer(
            f"Привет, {message.from_user.first_name}! 👋\n\n"
            "Добро пожаловать в наш интернет-магазин!\n\n"
            "Чтобы продолжить, нажми кнопку «Начать».",
            reply_markup=start_keyboard()
        )



@db.message(F.text == "🚀 Начать")
async def menu_handler(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_name)

    await message.answer(
        "Давай зарегистрируемся!\n\n"
        "Напиши своё имя и фамилию."
    )  
    


@db.message(F.text == "🛍 Категории")
async def categories_handler(message: Message):

    await message.answer(
        "🛍 Добро пожаловать в наши интернет-магазины!\n\n"
        "Выберите интересующую вас категорию товаров.\n",
        reply_markup=categories_keyboard()
    )    



async def main():
    init_db()  
    db.include_router(registration_router)
    
    print("Бот запущен. Ожидание сообщений...")
    
    await db.start_polling(bot)

    

if __name__ == "__main__":
    asyncio.run(main())