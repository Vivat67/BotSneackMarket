# from longpoll_bot import LongPollBot
from nlu_longpoll_bot import NLULongPollBot

if __name__ == '__main__':
    # Бот с клавиатурой и обучен на конфиге для ответа на простые вопросы
    nLULongPollBot = NLULongPollBot()
    nLULongPollBot.run_long_poll()
    # Бот только с клавиатурой
    # longpoll_bot = LongPollBot()
    # longpoll_bot.run_bot()
