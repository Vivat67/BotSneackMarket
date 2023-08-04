from peewee import *  # создаем базу данных заказов: импортируем библиотеку пиви
from config_db_snackmart import db


class Orders(Model):  # создаем поля таблицы
    id = AutoField()
    user_id = IntegerField()
    track_number_CDEK = IntegerField()
    phone_number = CharField()
    buyer_name = CharField(max_length=300)
    products = CharField(max_length=10000)
    status_order = CharField()

    class Meta:
        database = db
        table_name = 'orders'


def create_and_save_orders():
    db.connect()  # Подключаемся к базе данных
    db.create_tables([Orders])   # Создаем таблицу, если она еще не существует

    # Создаем экземпляры таблицы и сохраняем его в базе данных
    # (метод проверяет наличие в БД заказа)
    order, created = Orders.get_or_create(
        user_id=4466946,
        defaults={
            'track_number_CDEK': 1446921215,
            'phone_number': '+79113288554',
            'buyer_name': 'Артем',
            'products': '["Оленина ломтики - 1 кг", "Курица ломтики - 1 кг", "Консервы из оленины - 10 шт"]',
            'status_order': 'Вручен'
        }
    )

    order1, created1 = Orders.get_or_create(
        user_id=3323456,
        defaults={
            'track_number_CDEK': 1445637149,
            'phone_number': '+7723456789',
            'buyer_name': 'Витек',
            'products': '["Сухарики бородинские - 1 кг", "Пельмени из оленины - 2 упаковки", "Ерш вяленый - 1 кг"]',
            'status_order': 'Вручен'
        }
    )

    order2, created2 = Orders.get_or_create(
        user_id=213125699,
        defaults={
            'track_number_CDEK': 1439418472,
            'phone_number': '+79023339934',
            'buyer_name': 'Андрюха',
            'products': '["Сухарики бородинские - 300 кг", "Пельмени из оленины - 1000 упаковки", "Ерш вяленый филе - 10 кг"]',
            'status_order': 'Вручен'
        }
    )

    order3, created3 = Orders.get_or_create(
        user_id=21314377,
        defaults={
            'track_number_CDEK': 1435712195,
            'phone_number': '+79043299934',
            'buyer_name': 'Серый',
            'products': '["Сухарики бородинские - 30 кг",, "Ерш вяленый филе - 100 кг"]',
            'status_order': 'Вручен'
        }
    )

    order4, created4 = Orders.get_or_create(
        user_id=2131256,
        defaults={
            'track_number_CDEK': 1432720087,
            'phone_number': '+79933299934',
            'buyer_name': 'Надежда',
            'products': '["Лось ломтики - 312 кг", "Купаты из оленины - 100 упаковки"]',
            'status_order': 'Вручен'
        }
    )

    order5, created5 = Orders.get_or_create(
        user_id=2345667,
        defaults={
            'track_number_CDEK': 1425871478,
            'phone_number': '+7993329377',
            'buyer_name': 'Ахмед',
            'products': '["Свинина ломтики - 2300 кг"]',
            'status_order': 'Активный'
        }
    )

    db.close()  # Закрываем соединение с базой данных


def get_cdek_id_by_user_id(user_id):
    db.connect()
    # Ищем запись с указанным user_id в базе данных
    order = Orders.get_or_none(Orders.user_id == user_id)
    # Закрываем соединение с базой данных
    db.close()
    # Возвращаем найденное значение track_number_CDEK или None, если запись не найдена
    if order:
        return order.track_number_CDEK
    else:
        return None


if __name__ == "__main__":
    create_and_save_orders()
