import logging
from environs import Env

env = Env()
env.read_env()

try:
    BOT_TOKEN = env.str("BOT_TOKEN")
    MINIMUM_WORDS = env.int("MINIMUM_WORDS")
    BANWORD = env.str("BANWORD")
except:
    logging.critical(".env файл не найден! Создаю новый...")
    logging.critical("Прежде чем использовать бота, необходимо ввести токен в BOT_TOKEN=")

    with open(".env", "w") as f:
        f.write("BOT_TOKEN=token\nMINIMUM_WORDS=100\nBANWORD=None")