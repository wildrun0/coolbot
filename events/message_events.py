import random
import logging
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import ChatActionRule
from loader import bot
from states import SuperStates
from generator import WordsGenerator
from data.config import MINIMUM_WORDS


generator = WordsGenerator()
phrase = 'кул говори'


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def bot_invite(event: Message) -> None:
    action = event.action
    group_id = event.group_id
    if not action or not group_id:
        return
    await bot.state_dispenser.set(event.peer_id, SuperStates.NOT_ABLE_TALK)
    if action.member_id == -group_id:
        await event.answer(f"""
            👋Здравствуйте!
            Для работы мне нужно выдать доступ к переписке 📧
            Начну говорить когда наговорите {MINIMUM_WORDS} слов
            🪛Для сброса словарного запаса в беседе используйте команду "кул сброс" 
            (только администраторы, боту необх. права администратора)
        """)

  
@bot.on.chat_message(state=SuperStates.NOT_ABLE_TALK)
async def switch_to_able(event: Message) -> None:
    if len(generator.words_array[event.peer_id]) >= MINIMUM_WORDS:
        await bot.state_dispenser.set(event.peer_id, SuperStates.ABLE_TALK)
        logging.info(f"peer({event.peer_id}) state switched from NOT_ABLE_TALK to ABLE_TALK")


@bot.on.chat_message(text_lowered=phrase, state=SuperStates.ABLE_TALK)
async def cool_say(event: Message) -> None:
    generated_text = await generator.generate_message(event.peer_id)
    await event.answer(generated_text)
    logging.info(f"peer({event.peer_id}) used a cool_say func")


@bot.on.chat_message(text_lowered="кул сброс")
async def cool_reset(event: Message) -> None:
    generator.words_array[event.peer_id] = []
    await generator.write_file(event.peer_id, event.text)
    await bot.state_dispenser.set(event.peer_id, SuperStates.NOT_ABLE_TALK)
    await event.answer(f"""
        Словарный запас сброшен!📕🚫
        💬Чтобы я снова заговорил, напоминаю, необходимо наговорить на {MINIMUM_WORDS} сообщений.
    """)
    logging.info(f"peer({event.peer_id}) used cool_reset")


@bot.on.chat_message()
async def cool_events(event: Message) -> None:
    if random.randint(0,9) == 9 and event.state_peer.state == "SuperStates:0":
        generated_text = await generator.generate_message(event.peer_id)
        await event.answer(generated_text)
        logging.info(f"peer({event.peer_id}) used cool_rand_talk")
    if event.text.lower() != phrase:
        await generator.write_file(event.peer_id, event.text)
        logging.debug(f"peer({event.peer_id}) phrase written")