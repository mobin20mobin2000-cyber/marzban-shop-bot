# ==========================================================
# Zeus Shop VPN PRO
# broadcast.py
# Part 1/3
# ==========================================================

import asyncio

from telegram import Bot

from database import (
    get_all_users,
    save_broadcast_history
)


# ==========================================================
# Delay
# ==========================================================

SEND_DELAY = 0.05


# ==========================================================
# Broadcast
# ==========================================================

async def broadcast_message(

    bot: Bot,

    message: str

):

    users = get_all_users()

    success = 0

    failed = 0
    # ==========================================================
# Send Broadcast
# Part 2/3
# ==========================================================

    total = len(users)

    for user in users:

        try:

            await bot.send_message(

                chat_id=user["user_id"],

                text=message

            )

            success += 1

        except Exception:

            failed += 1

        await asyncio.sleep(SEND_DELAY)

    save_broadcast_history(

        message,

        success,

        failed

    )

    return {

        "total": total,

        "success": success,

        "failed": failed

    }
    # ==========================================================
# Zeus Shop VPN PRO
# broadcast.py
# Part 3/3
# ==========================================================


# ==========================================================
# Broadcast Photo
# ==========================================================

async def broadcast_photo(

    bot: Bot,

    photo,

    caption=""

):

    users = get_all_users()

    success = 0

    failed = 0

    total = len(users)

    for user in users:

        try:

            await bot.send_photo(

                chat_id=user["user_id"],

                photo=photo,

                caption=caption

            )

            success += 1

        except Exception:

            failed += 1

        await asyncio.sleep(SEND_DELAY)

    save_broadcast_history(

        caption,

        success,

        failed

    )

    return {

        "total": total,

        "success": success,

        "failed": failed

    }


# ==========================================================
# Broadcast Document
# ==========================================================

async def broadcast_document(

    bot: Bot,

    document,

    caption=""

):

    users = get_all_users()

    success = 0

    failed = 0

    total = len(users)

    for user in users:

        try:

            await bot.send_document(

                chat_id=user["user_id"],

                document=document,

                caption=caption

            )

            success += 1

        except Exception:

            failed += 1

        await asyncio.sleep(SEND_DELAY)

    save_broadcast_history(

        caption,

        success,

        failed

    )

    return {

        "total": total,

        "success": success,

        "failed": failed

    }


print("✅ Broadcast Module Loaded")
