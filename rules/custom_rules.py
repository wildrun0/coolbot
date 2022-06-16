from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class TextLowered(ABCRule[Message]):
    def __init__(self, lt: str):
        self.lt = lt

    # все приходящие text проверяем в ловеркейсе с нужным результатом
    # так удобнее проверять команды, чтобы не запариваться с регистрами
    async def check(self, event: Message) -> bool:
        return event.text.lower() == self.lt