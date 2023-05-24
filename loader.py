from vkbottle.bot import Bot
from data.config import BOT_TOKEN
from config import BotConfig
from loguru import logger
import logging

FORMAT = '%(asctime)s [coolbot] %(message)s'

bot = Bot(token=BOT_TOKEN)
BotConfig(bot).init()


logger.disable("vkbottle")
logging.basicConfig(encoding='utf-8', level=logging.INFO, format=FORMAT, handlers=[
    logging.FileHandler("coolbot.log"),
    logging.StreamHandler()
])
