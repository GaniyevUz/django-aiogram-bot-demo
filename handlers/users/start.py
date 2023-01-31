from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ChatType

from loader import dp, db


@dp.message_handler(CommandStart(), chat_type=[ChatType.PRIVATE])
async def bot_start(message: types.Message):
    user = message.from_user
    full_name = message.from_user.full_name
    chat = message.get_args() if message.get_args() else None

    if not db.select_user(telegram_id=user.id):
        db.add_user(user.first_name, user.last_name, user.id, chat)
        if message.get_args():
            db.can_send_message(chat, user.id)
            await message.answer(
                f"Salom, {full_name}! endi siz guruhda yoza olasiz,"
                f" buning uchun guruhga yana 1 ta odam qoshing")
        else:
            await message.answer(f"Salom, {full_name}!")
    else:
        await message.answer(f"Salom, {full_name}!")
