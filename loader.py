from vkbottle.bot import Bot
from data.config import BOT_TOKEN
from config import BotConfig
import logging

FORMAT = '%(asctime)s [coolbot] %(message)s'

bot = Bot(BOT_TOKEN)
BotConfig(bot)

logging.basicConfig(encoding='utf-8', level=logging.INFO, format=FORMAT, handlers=[
    logging.FileHandler("coolbot.log"),
    logging.StreamHandler()
])