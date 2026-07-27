# ==========================================================
# Zeus Shop VPN PRO
# broadcast.py
# Part 1/5
# ==========================================================


from database import get_all_users





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



        except Exception:


            failed += 1





    return {

        "success": success,

        "failed": failed

    }
