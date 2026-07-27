# ==========================================================
# Zeus Shop VPN PRO
# broadcast.py
# CLEAN VERSION
# ==========================================================


import sqlite3
from datetime import datetime


from database import get_all_users



DB_NAME = "zeus.db"





# ==========================================================
# Send Message To All Users
# ==========================================================


async def send_broadcast(

    bot,

    message

):


    users = get_all_users()


    success = 0

    failed = 0





    for user in users:


        try:


            await bot.send_message(

                chat_id=user["user_id"],

                text=message

            )


            success += 1





        except Exception as error:


            print(

                "BROADCAST ERROR:",

                error

            )


            failed += 1





    return {

        "success": success,

        "failed": failed,

        "total": len(users)

    }









# ==========================================================
# Professional Broadcast Message
# ==========================================================


async def send_broadcast_pro(

    bot,

    message

):


    text = f"""
👑 Zeus Shop VPN

━━━━━━━━━━━━━━

{message}

━━━━━━━━━━━━━━

❤️ ممنون از همراهی شما
"""



    return await send_broadcast(

        bot,

        text

    )









# ==========================================================
# Save Broadcast History
# ==========================================================


def save_broadcast_history(

    message,

    success,

    failed

):


    conn = sqlite3.connect(

        DB_NAME

    )


    cursor = conn.cursor()





    cursor.execute("""

    CREATE TABLE IF NOT EXISTS broadcasts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        message TEXT,

        success INTEGER,

        failed INTEGER,

        created_at TEXT

    )

    """)





    cursor.execute(

        """
        INSERT INTO broadcasts
        (
            message,
            success,
            failed,
            created_at
        )

        VALUES (?, ?, ?, ?)

        """,

        (

            message,

            success,

            failed,

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )





    conn.commit()

    conn.close()







# ==========================================================
# Final Broadcast
# ==========================================================


async def broadcast_message(

    bot,

    message

):


    result = await send_broadcast_pro(

        bot,

        message

    )





    save_broadcast_history(

        message,

        result["success"],

        result["failed"]

    )





    return result
