# Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.
import sqlite3
connection = sqlite3.connect('database_14.db')
cursor = connection.cursor()
# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
# initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# username - текст (не пустой)
# email - текст (не пустой)
# age - целое число (не пустой)
# balance - целое число (не пустой)
# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице
# Users, в противном случае False. Для получения записей используйте SQL запрос.
#
def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXIST Users(
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    );
    ''')

    cursor.execute('''
CREATE TABLE IF NOT Products(
id INT PRIMARY KEY ,
title TEXT NOT NULL,
description TEXT,
price INT NOT NULL
);
''')
    connection.commit()

initiate_db()

cursor.execute('''DELETE FROM Products''')
for i in range(1, 5):
    cursor.execute(('INSERT INTO Products (title, description, price) VALUES(?, ?, ?)'),
            (f'Product{i}', f'Описание {i}', {i*100}))


def get_all_products():
    cursor.execute(''' SELECT * FROM Products''')
    return cursor.fetchall()

def add_user(username, email, age):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, 1000)',
                   (username, email, age))



connection.commit()

def is_included(username):
    cursor.execute('''SELECT * FROM Users''')
    users = cursor.fetchall()
    for user in users:
        if user[1] == username:
            return True
    return False
connection.close()

# Изменения в Telegram-бот:
# Кнопки главного меню дополните кнопкой "Регистрация".

