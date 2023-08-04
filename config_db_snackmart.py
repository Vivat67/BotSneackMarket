# подключаемся к БД на phpMyAdmin
# создаем базу данных заказов: импортируем библиотеку пиви
from peewee import MySQLDatabase
db = MySQLDatabase(
    host="server102.hosting.reg.ru",
    user="u1450880_vlad",
    password="YourPass123",
    database="u1450880_vlad")
