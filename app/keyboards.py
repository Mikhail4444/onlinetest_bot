from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

task = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1: Функция суммы двух чисел `add(a, b)`', callback_data='1')],
    [InlineKeyboardButton(text='2: Функция разности двух чисел `sub(a, b)`', callback_data='2')],
    [InlineKeyboardButton(text='3: Функция произведения двух чисел `mul(a, b)`', callback_data='3')],
    [InlineKeyboardButton(text='4: Функция деления двух чисел `div(a, b)`', callback_data='4')]])