from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Предложка'
        )
    ],
    [
        KeyboardButton(
            text="Запросы на удаление"
        )
    ]
], resize_keyboard=True)


requests_check = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="Одобрить"
        ),
        KeyboardButton(
            text="Отклонить"
        )
    ],
    [
        KeyboardButton(
            text="Назад"
        )
    ]
], resize_keyboard=True)

requestsdel_check = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="Одобрить удаление"
        ),
        KeyboardButton(
            text="Отклонить удаление"
        )
    ],
    [
        KeyboardButton(
            text="Назад"
        )
    ]
], resize_keyboard=True)

y_n = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Да'
        ),
        KeyboardButton(
            text='Нет'
        )
    ]
], resize_keyboard=True)