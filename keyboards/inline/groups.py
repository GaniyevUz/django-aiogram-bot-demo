from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from loader import db


def get_keyboard(from_user_id, message_id):
    keyboard_markup = InlineKeyboardMarkup(row_width=4)
    keyboard_markup.add(InlineKeyboardButton('Hammaga Yuborish', callback_data=f'chat:all:{from_user_id}:{message_id}'))
    keys = []

    for _, chat_id, title, *args in db.get_all_chats():
        keys.append(InlineKeyboardButton(title, callback_data=f'chat:{chat_id}:{from_user_id}:{message_id}'))
    keyboard_markup.add(*keys)
    return keyboard_markup
