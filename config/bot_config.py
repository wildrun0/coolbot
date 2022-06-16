from rules import TextLowered
from states import SuperStates
from generator import WordsGenerator
from data.config import MINIMUM_WORDS

class BotConfig():
    async def states_init(self) -> None:                                    # инициализируем при старте бота нужный стейт у бесед
        for peer_id, peer_messages in WordsGenerator().words_array.items(): # в которых бот уже находится, это нужно чтобы 
            if len(peer_messages) >= MINIMUM_WORDS:                         # при запуске не возникало проблем с отсуствием стейта
                await self.bot.state_dispenser.set(peer_id, SuperStates.ABLE_TALK)
            else:
                await self.bot.state_dispenser.set(peer_id, SuperStates.NOT_ABLE_TALK)


    def __init__(self, bot):
        self.bot = bot
        self.bot.loop_wrapper.add_task(self.states_init)
        self.bot.labeler.custom_rules["text_lowered"] = TextLowered