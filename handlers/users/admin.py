from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils import exceptions as exc

from loader import dp, db
from root.settings import ADMINS
from utils import permissions
from utils.broadcast import broadcaster

RESTRICT_EXCEPTIONS = (
    exc.CantRestrictChatOwner, exc.CantRestrictSelf, exc.ChatAdminRequired, exc.NotEnoughRightsToRestrict)


@dp.message_handler(is_chat_admin=[ADMINS], commands=['broadcast'])
async def send_broadcast(msg: types.Message):
    pass
