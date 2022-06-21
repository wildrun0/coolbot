import random
import logging
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import ChatActionRule
from loader import bot
from rules import IsAdmin, TextLowered
from states import SuperStates
from generator import WordsGenerator
from data.config import MINIMUM_WORDS


generator = WordsGenerator()    # можно инициализировать класс с доп. аргументами (см generator/words_generator.py)
phrase = 'кул говори'   # фраза на которую реагирует бот


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def bot_invite(event: Message) -> None:
    action = event.action
    group_id = event.group_id
    if not action or not group_id:
        return
    if action.member_id == -group_id:   # проверяем, это нас пригласили или нет
        await event.answer(f"""
            👋Здравствуйте!
            Для работы мне нужно выдать доступ к переписке 📧
            Начну говорить когда наговорите {MINIMUM_WORDS} сообщений
            🪛Для сброса словарного запаса в беседе используйте команду "кул сброс" 
            (только администраторы, боту необх. права администратора)
        """)
        await bot.state_dispenser.set(event.peer_id, SuperStates.NOT_ABLE_TALK)
        await generator.write_file(event.peer_id, "")
        logging.info(f"bot invited in {event.peer_id}")


@bot.on.chat_message(text_lowered=phrase, state=SuperStates.ABLE_TALK)
async def cool_say(event: Message) -> None: # собственно, стандартная функция для генерации предложений
    generated_text = await generator.generate_message(event.peer_id)
    await event.answer(generated_text)
    logging.info(f"peer({event.peer_id}) used a cool_say func")


@bot.on.chat_message(TextLowered("кул сброс"), IsAdmin())   # неожиданный ход потому что нужно сначала проверить
async def cool_reset(event: Message) -> None:               # фразу, а только потом факт админства.
    generator.words_array[event.peer_id] = []
    await generator.write_file(event.peer_id, event.text)
    await bot.state_dispenser.set(event.peer_id, SuperStates.NOT_ABLE_TALK)
    # сбрасываем список, стейт, и сохраняем                 
    await event.answer(f"""
        Словарный запас сброшен!📕🚫
        💬Чтобы я снова заговорил, напоминаю, необходимо наговорить на {MINIMUM_WORDS} сообщений
    """)
    logging.info(f"peer({event.peer_id}) used cool_reset")


@bot.on.chat_message()
async def cool_events(event: Message) -> None:
    if random.randint(0,9) == 9 and event.state_peer.state == "SuperStates:0":  # рандомные вставки бота посреди диалога - тут
        generated_text = await generator.generate_message(event.peer_id)
        await event.answer(generated_text)
        logging.info(f"peer({event.peer_id}) used cool_rand_talk")
    if event.text.lower() != phrase:                                            # попутно сохраняем все сообщения из беседы
        await generator.write_file(event.peer_id, event.text)
        logging.debug(f"peer({event.peer_id}) phrase written")
    if event.state_peer.state == "SuperStates:1" and len(generator.words_array[event.peer_id]) >= MINIMUM_WORDS:
        await bot.state_dispenser.set(event.peer_id, SuperStates.ABLE_TALK)
        logging.info(f"peer({event.peer_id}) state switched from NOT_ABLE_TALK to ABLE_TALK")