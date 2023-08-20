"""
Модуль для создания простого бота с клавиатурой.
Применяется на платформе vk в сообществе СнэкМаркет.
"""

# работа с файловой системой
import os

# основной класс библотеки vk_api
import vk_api
# загрузка информации из .env-файла
from dotenv import load_dotenv
# клавиатура
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# работа с longpoll-сервером и отслеживание событий
from vk_api.longpoll import VkEventType, VkLongPoll
# загрузка вложений(изображение)
from vk_api.upload import VkUpload
# получение случайного id сообщения
from vk_api.utils import get_random_id

from cdek_tracking import CdekClient
from data_base_snackmart import get_cdek_id_by_user_id


class LongPollBot():
    """
    Бот, прослушивающий в бесконечном цикле входящие сообщения.
    Создает клавиатуру для пользователя.
    """

    # текущая сессия ВКонтакте
    vk_session = None

    # доступ к API ВКонтакте
    vk_api_access = None

    # пометка авторизованности
    authorized = False

    # длительное подключение
    longpoll = None

    # загрузка вложений (изоброжений)
    upload = None

    # ссылка на магазин
    STORE_ADDRESS = 'https://snackmart.ru/'

    def __init__(self):
        """
        Инициализация бота при помощи получения доступа к API ВКонтакте
        """
        # загрузка информации из .env-файла
        load_dotenv()

        # авторизация
        self.vk_api_access = self.do_auth()

        if self.vk_api_access is not None:
            self.authorized = True

        self.longpoll = VkLongPoll(self.vk_session)

        self.upload = VkUpload(self.vk_session)

        # создание клавиатуры
        self.keyboard = VkKeyboard()
        self.keyboard.add_openlink_button('Покажи что есть?',
                                          link=self.STORE_ADDRESS)
        self.keyboard.add_line()
        self.keyboard.add_button('Где мой заказ?',
                                 color=VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Предложение недели',
                                 color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_button('Контакты',
                                 color=VkKeyboardColor.NEGATIVE)

    def do_auth(self) -> None:
        """
        Авторизация сообщества. Использует переменную,
        хранящуюся в файле настроек окружения .env,
        в виде строки ACCESS_TOKEN=""

        Returns: возможность работать с API
        """
        token = os.getenv("ACCESS_TOKEN")
        try:
            self.vk_session = vk_api.VkApi(token=token)
            return self.vk_session.get_api()
        except Exception as error:
            print(error)

    def create_image(self, image: str) -> str:
        """
        Загрузка и подготовка изображения для использования.

        Args:
            image: ссылка на изображение.
        Returns:
            attachments[0]: изображение готовое для использования.
        """
        attachments = []
        upload_image = self.upload.photo_messages(photos=image)[0]
        attachments.append(
            'photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        return attachments[0]

    def contacts(self, user_id: int) -> None:
        """
        Ответ пользователю на ввод команды "Контакты"

        Args:
            user_id: id получателя сообщения
        """
        self.send_image(user_id, 'Попробуй найди...')

    def command_where(self, user_id: int):
        """
        Ответ пользователю на ввод команды "Где мой заказ?"

        Args:
            user_id: id получателя сообщения
        """
        cdek_client = CdekClient()
        cdek_client.authorize()
        # user_id=4466946 для примера
        cdek_number = str(get_cdek_id_by_user_id(user_id=4466946))
        cdek_info = cdek_client.get_order_info(cdek_number)
        print(cdek_info)
        self.send_msg(user_id, cdek_info)

    def command_offer_week(self, user_id: int) -> None:
        """
        Ответ пользователю на ввод команды "Предложение недели"

        Args:
            user_id: id получателя сообщения
        """
        self.send_sticker(user_id, '8014')

    def send_msg(self, user_id: int, message: str) -> None:
        """
        Отправка сообщения пользователю.
        Добавляет клавиатуру.

        Args:
            user_id: id получателя сообщения
            message: текст сообщения
            random_id: случайны id сообщения
            keyboard: клавиатура
        """
        self.vk_session.method('messages.send', {
                               'user_id': user_id,
                               'message': message,
                               'random_id': get_random_id(),
                               'keyboard': self.keyboard.get_keyboard()
                               })

    def send_image(self, user_id: int, message: str) -> None:
        """
        Отправка сообщения пользователю.
        Добавляет изображение.

        Args:
            user_id: id получателя сообщения
            message: текст сообщения
            random_id: случайны id сообщения
            attachment: изображение
        """
        self.vk_session.method('messages.send', {
                               'user_id': user_id,
                               'message': message,
                               'random_id': get_random_id(),
                               'attachment': self.create_image(
                                            'image/ebenya.webp')
                               })

    def send_sticker(self, user_id: int, sticker_id: int) -> None:
        """
        Отправка стикера пользователю.

        Args:
            user_id: id получателя сообщения
            sticker_id: id стикера
            random_id: случайны id сообщения
        """
        self.vk_session.method('messages.send', {
                               'user_id': user_id,
                               'sticker_id': sticker_id,
                               'random_id': get_random_id()})

    def run_bot(self) -> None:
        """
        Запуск бота.
        """
        print('Бот запущен!')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Где мой заказ?':
                    self.command_where(event.user_id)
                elif event.text == 'Предложение недели':
                    self.command_offer_week(event.user_id)
                elif event.text == 'Контакты':
                    self.contacts(event.user_id)
