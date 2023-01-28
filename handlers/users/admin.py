from aiogram import types
from loader import dp, db, bot
from utils.broadcast import broadcaster
from aiogram.dispatcher import FSMContext
from keyboards.inline.groups import get_keyboard
from aiogram.dispatcher.filters.state import StatesGroup, State


class Broadcast(StatesGroup):
    start = State()
    message = State()


@dp.message_handler(commands=['broadcast'])
async def send_broadcast(msg: types.Message):
    await Broadcast.start.set()
    await msg.answer('Yubormoqchi bolgan xabarmi menga yuboring')


@dp.message_handler(state=Broadcast.start, content_types=types.ContentTypes.ANY)
async def send_broadcast(msg: types.Message, state: FSMContext):
    await msg.reply('Yubormoqchi bolgan chatlarni belgilang',
                    reply_markup=get_keyboard(msg.from_user.id, msg.message_id))
    await Broadcast.next()


@dp.callback_query_handler(state=Broadcast.message)
async def send_broadcast(query: types.CallbackQuery, state: FSMContext):
    # await state.update_data(message=(msg.from_user.id, msg.message_id))
    _, chat_id, from_user_id, message_id = query.data.split(':')

    chat_id = db.select_all_users if chat_id == 'all' else db.select_all_chat_users(chat_id)

    await bot.send_message(from_user_id, 'Habar yuborish boshlandi')
    count = await broadcaster(chat_id, from_user_id, message_id)

    p = round((count * 100) / len(chat_id), 2) if len(chat_id) > 0 else 0
    await bot.send_message(from_user_id,
                           f"{len(chat_id)}tadan {count}ta odamga yuborildi {p}%")
    await state.finish()
