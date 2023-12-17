from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Личный кабинет'
        ),
        KeyboardButton(
            text='Предложить запись'
        )
    ],
    [
        KeyboardButton(
            text='Запрос на удаление'
        )
    ]
], resize_keyboard=True)


file_type = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Фото'
        ),
        KeyboardButton(
            text='Видео'
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