from pprint import pprint
from datetime import datetime
import requests

# Параметры авторизации клиента
client_id = "5wf50vc39NELIQBP3OntHZPqW2i8KqIw"
client_secret = "gQG79qjAXWZVR16cxtwIpD0vMWEYlAIR"
grant_type = "client_credentials"

# URL для отправки запроса авторизации
auth_url = "https://api.cdek.ru/v2/oauth/token?parameters"

# Параметры запроса авторизации
auth_data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": grant_type
}

# Отправка POST-запроса для авторизации
auth_response = requests.post(auth_url, data=auth_data)

# Проверка статуса ответа авторизации
if auth_response.status_code == 200:
    # Получение данных из ответа авторизации
    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]

    # URL и номер заказа СДЭК
    url = "https://api.cdek.ru/v2/orders?cdek_number={cdek_number}"
    cdek_number = "1438512853"

    # Добавление access_token к заголовкам запроса
    headers = {
        "Authorization": "Bearer " + access_token
    }

    # Отправка GET-запроса по номеру заказа СДЭК
    response = requests.get(url.format(cdek_number=cdek_number), headers=headers)
    data = response.json()

    # Обработка ответа
    if response.status_code == 200:
        # Информация о заказе
        print("Информация о заказе:")
        last_status = (data['entity']['statuses'][0])
        city = last_status['city']
        date_time = last_status['date_time']
        name = last_status['name']
        # Исходная строка с датой и временем
        original_datetime = date_time
        # Преобразование строки в объект datetime
        dt = datetime.strptime(original_datetime, '%Y-%m-%dT%H:%M:%S%z')
        # Преобразование объекта datetime в требуемый формат
        formatted_datetime = dt.strftime('%d.%m.%Y в %H:%M ')
        # Вывод результата
        print(f"{formatted_datetime}\nГород/населенный пункт: {city}\nСтатус заказа: {name}")
    else:
        # Обработка ошибки
        print("Ошибка при получении информации о заказе:", response.status_code, data)
else:
    print("Ошибка при выполнении запроса авторизации:", auth_response.status_code)
