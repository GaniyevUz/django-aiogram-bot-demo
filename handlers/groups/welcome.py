import asyncio
import logging

from aiogram import types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ChatType
from aiogram.utils import exceptions as exc
from aiogram.utils.deep_linking import get_start_link

from loader import dp, db, bot
from utils import permissions

RESTRICT_EXCEPTIONS = (
    exc.CantRestrictChatOwner, exc.CantRestrictSelf, exc.ChatAdminRequired, exc.NotEnoughRightsToRestrict)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('welcome')


@dp.message_handler(content_types=types.ContentType.TEXT, chat_type=[ChatType.SUPERGROUP])
async def message_checker(msg: types.Message):
    user_id = msg.from_user.id
    chat_id = msg.chat.id
    count_invitation, can_send_message = db.count_invitation(chat_id, user_id)
    invite_user_limit = db.get_invite_user_limit(chat_id)

    try:
        if count_invitation >= invite_user_limit and can_send_message:
            await msg.chat.restrict(user_id=user_id, permissions=permissions.FREE)
            # await msg.reply(f'{msg.from_user.full_name} siz endi guruhda yozishingiz mumkin')
        elif count_invitation >= invite_user_limit and not can_send_message:
            link = await get_start_link(chat_id)
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Botga start bosing', url=link))
            await bot.send_message(chat_id, f'{msg.from_user.full_name} guruhda yozishingiz uchun botga azo boling',
                                   reply_markup=keyboard)
        else:
            await msg.chat.restrict(user_id=user_id, permissions=permissions.RESTRICTED)
            # await asyncio.sleep(.10)
            log.info(f"Target [ID:{user_id}]: success")
            await msg.answer(f'🔄Sizning umumiy ball: <b>{count_invitation}</b>\n'
                             f'⚠️Guruhda yozish uchun sizda <b>{invite_user_limit} ball</b> bo\'lishi kerak',
                             parse_mode=ParseMode.HTML)

    except RESTRICT_EXCEPTIONS:
        pass


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def restrict_new_chat_member(msg: types.Message):
    user = msg.from_user
    user_id = user.id
    chat_id = msg.chat.id
    # chat = db.get_chat(chat_id=msg.chat.id)
    if not db.get_chat(chat_id=chat_id):
        db.new_chat(chat_id, msg.chat.username, msg.chat.title)
    new_count = len(msg.new_chat_members)
    count_invitation, can_send_message = db.count_invitation(chat_id, user_id)
    invite_user_limit = db.get_invite_user_limit(chat_id)
    count_invitation += new_count
    db.increase_invitation(chat_id, user_id, count_invitation)
    await bot.send_message(chat_id,
                           f'🆕{user.full_name} siz guruhga {new_count}ta odam qoshdingiz.\n'
                           f'🔄Sizning umumiy ball: <b>{count_invitation}</b>\n'
                           f'⚠️Guruhda yozish uchun sizda <b>{invite_user_limit} ball</b> bo\'lishi kerak',
                           parse_mode=ParseMode.HTML)

    try:
        if count_invitation >= invite_user_limit and can_send_message:
            await msg.chat.restrict(user_id=user.id, permissions=permissions.FREE)
            await msg.reply(f'{user.full_name} siz endi guruhda yozishingiz mumkin')
        elif count_invitation >= invite_user_limit and not can_send_message:
            link = await get_start_link(chat_id)
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Botga start bosing', url=link))
            await bot.send_message(chat_id, f'{user.full_name} guruhda yozishingiz uchun botga azo boling',
                                   reply_markup=keyboard)
    except RESTRICT_EXCEPTIONS:
        pass

#
# @dp.message_handler(commands=['mystat'])
# async def mystats(msg: types.Message):
#     user_id = msg.from_user.id
#     chat_id = msg.chat.id
#     count_invitation, can_send_message = db.count_invitation(chat_id, user_id)
#     invite_user_limit = db.get_invite_user_limit(chat_id)
#     await msg.reply(f'🔄Sizning umumiy ball: <b>{count_invitation}</b>')
