 # Дополните ранее написанный код для Telegram-бота:
# Создайте файл crud_functions.py и напишите там следующие функции:
import sqlite3
connection = sqlite3.connect('database_14.db')
cursor = connection.cursor()

# которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# title(название продукта) - текст (не пустой)
# description(описание) - текст
# price(цена) - целое число (не пустой)

def initiate_db():

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


connection.commit()
connection.close()

# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
#
# Изменения в Telegram-бот:
# В самом начале запускайте ранее написанную функцию get_all_products.
# Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо
# обычной нумерации продуктов функцию get_all_products.
# Полученные записи используйте в выводимой надписи: "Название: <title> | Описание: <description>
 # | Цена: <price>"

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)