from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message
from vkbottle import VKAPIError

class IsAdmin(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        try:
            members = await event.ctx_api.messages.get_conversation_members(
                peer_id=event.peer_id
            )
            admins = [member.member_id for member in members.items if member.is_admin]
            from_id = event.from_id
            if from_id in admins:
                return True
        except VKAPIError[917]:
            await event.answer("🚫Для выполнения этой команды мне необходимы права администратора")
            return False