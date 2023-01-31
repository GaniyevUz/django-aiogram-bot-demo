import asyncio
import logging

from aiogram.utils import exceptions

from loader import bot

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


async def copy_message(user_id: int, from_user_id: int, message_id: int) -> bool:
    """
    Safe messages sender

    :param message_id:
    :param from_user_id:
    :param user_id:
    :return:
    """
    try:
        await bot.copy_message(user_id, from_user_id, message_id)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.CantInitiateConversation:
        log.error(f"Target [ID:{user_id}]: bot can't initiate conversation with a user")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await copy_message(user_id, from_user_id, message_id)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(users: list, from_user_id: int, message_id: int) -> int:
    """
    Simple broadcaster

    :return: Count of messages
    """
    count = 0
    try:
        for user_id in users:
            print()
            if await copy_message(user_id[0], from_user_id, message_id):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)

    finally:
        log.info(f"{count} messages successful sent.")

    return count
