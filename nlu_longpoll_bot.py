"""
Модуль добавляет классу LongPollBot дополнительный
функционал для обработки часто встречающихся вопросов.
"""
# представление в качестве JSON
import json
# для генерации случайных ответов
import random

# для векторизации текста
from sklearn.feature_extraction.text import TfidfVectorizer
# для классификации намерений
from sklearn.linear_model import LogisticRegression
# использование VkEventType
from vk_api.longpoll import VkEventType

# базовый класс бота из файла longpoll_bot
from longpoll_bot import LongPollBot


class NLULongPollBot(LongPollBot):
    """
    Бот, прослушивающий в бесконечном цикле входящие сообщения,
    способен отвечать на них.
    Бот обучен на заданном конфиге.
    """

    # векторизатор текста
    vectorizer = None

    # классификатор запросов
    classifier = None

    # порог вероятности, при котором на намерение пользователя
    # будет отправляться ответ из bot_config
    threshold = 0.4

    # ведение статистики ответов
    stats = {'intent': 0, 'generative': 0, 'failure': 0}

    def __init__(self):
        """
        Иинициализация бота.
        """
        super().__init__()

        # Загрузка конфига из файла
        with open('bot_config.json', encoding='utf-8') as file:
            self.bot_config = json.load(file)

        # обучение бота
        self.create_bot_config_corpus()

    def run_long_poll(self) -> None:
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
                else:
                    bot_response = self.get_bot_response(event.text)
                    self.send_msg(user_id=event.user_id, message=bot_response)

                    # вывод статистики
                    print(self.stats)

    def get_bot_response(self, request: str) -> str:
        """
        Отправка ответа пользователю на его запрос с учётом статистики.

        Args:
            request: запрос пользователя
        Returns:
            ответ для пользователя
        """
        # определение намерения пользователя,
        # использование заготовленного ответа
        intent = self.get_intent(request)
        if intent:
            self.stats['intent'] += 1
            return self.get_response_by_intent(intent)

        # если бот не может подобрать ответ - отправляется ответ-заглушка
        self.stats['failure'] += 1
        return self.get_failure_phrase()

    def get_intent(self, request: str) -> str:
        """
        Получение наиболее вероятного намерения пользователя из сообщения.

        Args:
            request: запрос пользователя
        Returns:
            best_intent: наилучшее совпадение
        """
        question_probabilities = self.classifier.predict_proba(
            self.vectorizer.transform([request]))[0]
        best_intent_probability = max(question_probabilities)

        if best_intent_probability > self.threshold:
            best_intent_index = list(question_probabilities).index(
                                            best_intent_probability)
            best_intent = self.classifier.classes_[best_intent_index]
            return best_intent

    def get_response_by_intent(self, intent: str) -> str:
        """
        Получение случайного ответа на намерение пользователя.

        Args:
            intent: намерение пользователя
        Returns:
            случайный ответ из прописанных для намерения
        """
        phrases = self.bot_config['intents'][intent]['responses']
        return random.choice(phrases)

    def get_failure_phrase(self) -> str:
        """
        Если бот не может ничего ответить - будет отправлена случайная фраза
        из списка failure_phrases в bot_config.

            Returns:
                случайная фраза в случае провала подбора ответа ботом
        """
        phrases = self.bot_config['failure_phrases']
        return random.choice(phrases)

    def create_bot_config_corpus(self) -> None:
        """
        Создание и обучение корпуса для бота, обученного на bot_config
        для дальнейшей обработки запросов пользователя.
        """
        corpus = []
        y = []

        for intent, intent_data in self.bot_config['intents'].items():
            for example in intent_data['examples']:
                corpus.append(example)
                y.append(intent)

        # векторизация
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
        x = self.vectorizer.fit_transform(corpus)

        # классификация
        self.classifier = LogisticRegression()
        self.classifier.fit(x, y)

        print('Обучение на файле конфигурации завершено')
