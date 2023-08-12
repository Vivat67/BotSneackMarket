"""
    Данный код создаёт модель c помощью библиотеки Peewee под названием Orders,
    которая представляет собой таблицу для хранения информации о заказах из
    магазина ВК в базе данных на сервере phpMyAdmin.

    В Orders определены поля, такие как id, user_id, track_number_CDEK,
    phone_number, buyer_name, products и status_order.

    Код включает функцию create_and_save_orders(), которая создаёт и сохраняет
    экземпляры таблицы Ordersв базе данных, и функцию
    get_cdek_id_by_user_id(user_id), которая позволяет получить номер
    отслеживания CDEK на основе предоставленного user_id.
    Основная часть кода инициализирует таблицы базы данных и создаёт
    несколько примеров заказов с использованием метода get_or_create().

    Примечание: Для корректной работы кода необходимо предоставить соединение
    с базой данных и конфигурацию (config_db_snackmart).
"""
from peewee import AutoField, CharField, IntegerField, Model

from config_db_snackmart import db


class Orders(Model):
    """
    Создание таблицы на сервере phpMyAdmin
    помощью библиотеки Peewee под c с названием Orders с полями: id, user_id,
    track_number_CDEK, phone_number, buyer_name, products и status_order.
    """
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


def get_cdek_id_by_user_id(user_id) -> str:
    """
    Функция get_cdek_id_by_user_id(user_id) позволяет получить номер
    отслеживания CDEK для последующей проверки в функуии get_order_info.
    """
    db.connect()
    # Ищем запись с указанным user_id в базе данных
    order = Orders.get_or_none(Orders.user_id == user_id)
    # Закрываем соединение с базой данных
    db.close()
    # Возвращаем найденное значение track_number_CDEK или None,
    # если запись не найдена
    if order:
        return order.track_number_CDEK
