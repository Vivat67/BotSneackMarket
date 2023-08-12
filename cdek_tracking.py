import os

import requests
from dotenv import load_dotenv


class CdekClient:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token = None

    def authorize(self):
        """
        Этот метод выполняет процесс аутентификации OAuth 2.0 для получения
        токена доступа от CDEK API.

        Токен доступа необходим для осуществления аутентифицированных
        запросов к API.
        Если авторизация успешна, токен доступа сохраняется в атрибуте
        access_token экземпляра класса.

        Returns: self.access_token : возможность работы с API CDEK
        """

        grant_type = "client_credentials"
        auth_url = "https://api.cdek.ru/v2/oauth/token?parameters"
        auth_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": grant_type,
        }
        auth_response = requests.post(auth_url, data=auth_data)

        if auth_response.status_code == 200:
            auth_response_data = auth_response.json()
            self.access_token = auth_response_data["access_token"]
            return self.access_token
        return (
            "Ошибка при выполнении запроса авторизации:",
            auth_response.status_code,
        )

    def get_order_info(self, cdek_number: str) -> str:
        """
        Этот метод получает информацию о заказе по предоставленному
        трек-номеру CDEK (cdek_number).

        Для использования этого метода клиент должен быть авторизован, то есть
        метод authorize должен быть успешно
        вызван перед его использованием.
        Метод отправляет GET-запрос к CDEK API, передавая трек-номер и токен
        доступа в заголовках запроса.
        Затем он разбирает JSON-ответ и извлекает информацию о заказе,
        такую как последний статус, город и дата/время.

        Args:
            cdek_number: трек-номер заказа в СДЕК
        Returns:
           order_info : информация о заказе.
        """

        url = f"https://api.cdek.ru/v2/orders?cdek_number={cdek_number}"
        headers = {"Authorization": "Bearer " + self.access_token}
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            last_status = data["entity"]["statuses"][0]
            city = last_status["city"]
            date_time = last_status["date_time"]
            name = last_status["name"]
            original_datetime = date_time
            order_info = (
                f"Информация о заказе:\n"
                f"{original_datetime}\n"
                f"Город/населенный пункт: {city}\n"
                f"Статус заказа: {name}"
            )
            return order_info
        else:
            return (
                "Ошибка при получении информации о заказе:",
                response.status_code,
                data,
            )
