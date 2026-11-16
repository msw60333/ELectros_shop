
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🛍 Категории"),
                KeyboardButton(text="🛒 Корзина")
            ],
            [
                KeyboardButton(text="💳 Оплата")
            ]
        ],
        resize_keyboard=True
    )


CATEGORIES = [
    ("📱 Техника", "electronics"),
    ("🧸 Игрушки", "toys"),
    ("🏠 Всё для дома", "home"),
    ("⌚ Аксессуары", "accessories"),
    ("👕 Одежда", "clothes"),
    ("🎒 Всё для школы", "school"),
    ("🍽 Посуда", "dishes"),
    ("👟 Обувь", "shoes"),
    ("🔧 Инструменты", "tools"),
    ("🌳 Всё для дачи", "garden"),
]


# Временно указываем адреса-заглушки.
# Позже заменим их настоящими ссылками друга.

CATEGORY_URLS = {
    "electronics": "https://example.com/electronics",
    "toys": "https://example.com/toys",
    "home": "https://example.com/home",
    "accessories": "https://example.com/accessories",
    "clothes": "https://example.com/clothes",
    "school": "https://example.com/school",
    "dishes": "https://example.com/dishes",
    "shoes": "https://example.com/shoes",
    "tools": "https://example.com/tools",
    "garden": "https://example.com/garden",
}


def categories_keyboard():
    keyboard = []

    for name, category_id in CATEGORIES:
        keyboard.append([
            InlineKeyboardButton(
                text=name,
                url=CATEGORY_URLS[category_id]
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
