from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions_14_4 import *
from m_14_5 import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

Inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data='calories'),
        InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas')]
    ],resize_keyboard=True
)
Inline_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= "Product1", callback_data="product_buying"),
    InlineKeyboardButton(text= "Product2", callback_data="product_buying"),
    InlineKeyboardButton(text= "Product3", callback_data="product_buying"),
    InlineKeyboardButton(text= "Product4", callback_data="product_buying")]
    ]
)

# Изменения в Telegram-бот:
# Кнопки главного меню дополните кнопкой "Регистрация".
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация'), KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Купить'), KeyboardButton(text= 'Регистрация')]
    ], resize_keyboard=True
)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Напишите новый класс состояний RegistrationState с следующими объектами класса State:
    # username, email, age, balance(по умолчанию 1000).
    # Создайте цепочку изменений состояний RegistrationState.
    # Фукнции цепочки состояний RegistrationState:
    # sing_up(message):
    # Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
    # Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".

class RegistrationState(StatesGroup):
    username= State()
    email = State
    age = State()
    balance = State('1000')
# Фукнции# RegistrationState:
# sing_up(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
# Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя:")
    print("Введите имя пользователя:")
    await RegistrationState.username.set()
# set_username(message, state):
    # Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
    # Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
    # Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
    # Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует,
    # введите другое имя" и запрашивать новое состояние для RegistrationState.username.
@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        print("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        print("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
# set_email(message, state):
    # Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
    # Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
    # Далее выводить сообщение "Введите свой возраст:":
    # После ожидать ввода возраста в атрибут RegistrationState.age.\
@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    print("Введите свой возраст:")
    await RegistrationState.age.set()

# set_age(message, state):
    # Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
    # Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
    # Далее брать все данные (username, email и age)
    # из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
    # В конце завершать приём состояний при помощи метода finish().
    # Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
@@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    if 120 >= int(message.text) >= 0:
        await state.update_data(age=message.text)
        data = await state.get_data()
        add_user(data['username'], data['email'], data['age'])
        await message.answer('Регистрация успешна!')
        print('Регистрация успешна!')
    else:
        await message.answer('Введите коректный возраст')
        print('Введите коректный возраст')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Добро пожаловать ', reply_markup = start_kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for index, product in enumerate(get_all_products()):
        await message.answer(f'Название:Продукт{product[1]} | Описание: описание {product[2]} '
                             f'| Цена: {product [3]}')
        print(f'Название:Продукт{product[1]} | Описание: описание {product[2]} | Цена: {product[3]}')
        with open(f'{index+1}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup = Inline_KB)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = Inline_kb)
# Создайте новую функцию get_formulas(call), которая:
# Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
# Будет присылать сообщение с формулой Миффлина-Сан Жеора.
@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора для мужчин:\n'
                            '10 х вес(кг) + 6.25 х рост(см) - 5 х возраст + 5\n'
                              'Формула Миффлина-Сан Жеора для женщин:\n'
                              '10 х вес(кг) + 6.25 х рост(см) - 5 х возраст -161')
    await call.answer()

@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])

    man = 10 * weight + 6.25 * growth - 5 * age + 5
    woman = 10 * weight + 6.25 * growth - 5 * age - 161

    await UserState.weight.set()
    await message.answer(f"Норма калорий для мужчин: {man}")
    await message.answer(f"Норма калорий для женщин: {woman}")

    await state.finish()


    # set_age(message, state):
    # Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
    # Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
    # Далее брать все данные (username, email и age)
    # из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
    # В конце завершать приём состояний при помощи метода finish().
    # Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
