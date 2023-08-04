from peewee import Model, AutoField, IntegerField, CharField
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


def get_cdek_id_by_user_id(user_id):
    db.connect()
    # Ищем запись с указанным user_id в базе данных
    order = Orders.get_or_none(Orders.user_id == user_id)
    # Закрываем соединение с базой данных
    db.close()
    # Возвращаем найденное значение track_number_CDEK или None,
    # если запись не найдена
    if order:
        return order.track_number_CDEK
    else:
        return None
