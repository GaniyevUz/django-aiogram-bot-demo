from aiogram.types import ChatPermissions

RESTRICTED = ChatPermissions(can_send_messages=False,
                             can_send_media_messages=False,
                             can_send_other_messages=False,
                             can_add_web_page_previews=False,
                             can_invite_users=True,
                             )
FREE = ChatPermissions(can_send_messages=True,
                       can_send_media_messages=True,
                       can_send_other_messages=True,
                       can_add_web_page_previews=True,
                       can_invite_users=True,
                       can_send_polls=True,
                       )

