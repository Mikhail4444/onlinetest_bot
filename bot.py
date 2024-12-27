import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb

# Инициализация бота и диспетчера
bot = Bot(token='7648687187:AAHKfDrC1gFT41T4kw6hhSB2eid2LNe_CIQ')
dp = Dispatcher()

# Пример задания
tasks = {
    1: "Напишите функцию, которая возвращает сумму двух чисел. Название функции: `add(a, b)`.",
    2: "Напишите функцию, которая возвращает разность двух чисел. Название функции: `sub(a, b)`.",
    3: "Напишите функцию, которая возвращает произведение двух чисел. Название функции: `mul(a, b)`.",
    4: "Напишите функцию, которая возвращает частное двух чисел. Название функции: `div(a, b)`.",
}

# Сохранение заданий для пользователей
user_tasks = {}

# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет! Я бот для тестирования Python-кода. Введите /task, чтобы получить задание.")

# Команда /task — отправить задание
@dp.message(Command("task"))
async def task(message: Message):
    await message.reply(f"Выберите задание: ", reply_markup=kb.task)

# Обработка нажатий на клавиатуру
@dp.callback_query()
async def choose_task(callback: CallbackQuery):
    user_id = callback.from_user.id
    task_id = int(callback.data)
    if task_id in tasks:
        user_tasks[user_id] = task_id
        await callback.answer('Выбор принят!', show_alert=True)
        await callback.message.answer(f'Вы выбрали задание {task_id}: {tasks[task_id]}\nТеперь отправьте код решения.')
    else:
        await callback.answer('Ошибка выбора!', show_alert=True)
        await callback.message.answer("Некорректный выбор задания.")

# Проверка кода
def check_code(user_code: str, task_id: int) -> str:
    test_cases = {
        1: [(1, 2, 3), (0, 0, 0), (-1, -2, -3)],
        2: [(5, 3, 2), (0, 1, -1), (-1, -1, 0)],
        3: [(2, 3, 6), (0, 5, 0), (-2, -3, 6)],
        4: [(6, 2, 3), (5, 0, "ZeroDivisionError"), (-9, -3, 3)],
    }

    try:
        # Выполняем пользовательский код
        local_vars = {}
        exec(user_code, {}, local_vars)

        # Получаем имя функции в зависимости от задания
        function_name = {
            1: "add",
            2: "sub",
            3: "mul",
            4: "div",
        }.get(task_id)
        
        user_function = local_vars.get(function_name)

        if not callable(user_function):
            return f"Ошибка: функция `{function_name}` не определена."

        # Тестирование функции
        for x, y, expected in test_cases[task_id]:
            try:
                result = user_function(x, y)
                if result != expected:
                    return f"Ошибка: тест {x}, {y} провален. Ожидалось {expected}, получено {result}."
            except ZeroDivisionError:
                if expected != "ZeroDivisionError":
                    return f"Ошибка: тест {x}, {y} провален. Ожидалось {expected}, но возникло деление на ноль."

        return "Все тесты пройдены успешно!"

    except Exception as e:
        return f"Ошибка выполнения кода: {e}"

# Приём кода от пользователя
@dp.message()
async def handle_code(message: Message):
    user_id = message.from_user.id
    task_id = user_tasks.get(user_id)

    if not task_id:
        await message.reply("Вы ещё не получили задание. Используйте команду /task.")
        return

    user_code = message.text
    result = check_code(user_code, task_id)
    await message.reply(result)

async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')