from aiogram import Router , F
from aiogram.fsm.state import State , StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from database.db import get_db_connection 

router = Router()

class Registration(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_address = State()
    

def phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Поделиться номером телефона",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    

@router.message(Registration.waiting_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else ""
    
    if len(name) < 2 or len(name) > 30:
        await message.answer("Пожалуйста, введите корректное имя ")
        return
    
    await state.update_data(name=name)
    await state.set_state(Registration.waiting_phone)
    
    await message.answer(
        "Отлично! Теперь, пожалуйста, поделитесь своим номером телефона.",
        reply_markup=phone_keyboard()
    )
    
    
@router.message(Registration.waiting_name)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else ""

    if len(name) < 2 or len(name) > 100:
        await message.answer("Пожалуйста, введи корректное имя.")
        return

    await state.update_data(name=name)
    await state.set_state(Registration.waiting_phone)

    await message.answer(
        "Отлично! Теперь поделись номером телефона.",
        reply_markup=phone_keyboard()
    )



@router.message(Registration.waiting_phone)
async def get_phone(message: Message, state: FSMContext):

    
    if not message.contact:
        await message.answer(
            "Пожалуйста, нажми кнопку 📱 "
            "«Поделиться номером телефона».\n\n"
            "Нужно отправить именно контакт, а не написать номер текстом."
        )
        return

    contact = message.contact

    
    if contact.user_id != message.from_user.id:
        await message.answer(
            "Пожалуйста, поделись собственным номером телефона."
        )
        return

    await state.update_data(phone=contact.phone_number)
    await state.set_state(Registration.waiting_address)

    await message.answer(
        "✅ Номер телефона получен!\n\n"
        "Теперь напиши свой адрес доставки.",
        reply_markup=ReplyKeyboardRemove()
    )



@router.message(Registration.waiting_address)
async def get_address(message: Message, state: FSMContext):

    print("Получено сообщение с адресом!")

    address = message.text.strip() if message.text else ""

    if len(address) < 5 or len(address) > 300:
        await message.answer(
            "Пожалуйста, введи корректный адрес (от 5 до 300 символов)."
        )
        return

    data = await state.get_data()

    try:
        with get_db_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (
                    telegram_id, name, phone, address
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    name = excluded.name,
                    phone = excluded.phone,
                    address = excluded.address
                """,
                (
                    message.from_user.id,
                    data["name"],
                    data["phone"],
                    address
                )
            )

        await state.clear()

        await message.answer(
            "🎉 Регистрация успешно завершена!\n\n"
            f"Имя: {data['name']}\n"
            f"Телефон: {data['phone']}\n"
            f"Адрес: {address}\n\n"
            "Добро пожаловать в наш магазин!"
        )

        print("Пользователь успешно зарегистрирован!")

    except Exception as error:
        print(f"Ошибка сохранения пользователя: {error}")

        await message.answer(
            "Произошла ошибка при сохранении данных. "
            "Попробуй ещё раз."
        )
