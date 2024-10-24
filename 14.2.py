import sqlite3
connection = sqlite3.connect('not_tg.db')
cursor = connection.cursor()

cursor.execute('''
CREATE  TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)          
''')

# for i in range(1, 11):
#     cursor.execute(''' INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)''',
#                    (f'newuser{i}',  f'{i}eample@gmail.com', f'{i*10}', '1000'))

for i in range(1, 11, 2):
    cursor.execute('''UPDATE Users SET balance = ? WHERE username = ? ''', (500, f'User{i}'))
total2 = cursor.fetchall()
print(total2)

for i in range(1, 10, 3):
    cursor.execute('''DELETE FROM Users WHERE username = ? ''', (f'User{i}',))
# cursor.execute('''SELECT * FROM Users WHERE age != 60''')
# total = cursor.fetchall()
# for user in total:
#     print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')


# Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute('''DELETE FROM Users WHERE id = ? ''', (6,))

# Подсчитать общее количество записей.
cursor.execute('''SELECT COUNT(*) FROM Users''')
count_users = cursor.fetchone()[0]
print(count_users)

# Посчитать сумму всех балансов.
cursor.execute('''SELECT SUM(balance) FROM Users''')
sum_balance = cursor.fetchone()[0]
print(sum_balance)

# Вывести в консоль средний баланс всех пользователей.
cursor.execute('''SELECT AVG(balance) FROM Users''')
avg_balance = cursor.fetchone()[0]
print(avg_balance)

print(sum_balance / avg_balance)

connection.commit()
connection.close()
#
#
#
# Пример результата выполнения программы:
# Выполняемый код:
# # Код из предыдущего задания
# # Удаление пользователя с id=6
# # Подсчёт кол-ва всех пользователей
# # Подсчёт суммы всех балансов
# print(all_balances / total_users)
# connection.close()
#
# Вывод на консоль:
# 700.0
