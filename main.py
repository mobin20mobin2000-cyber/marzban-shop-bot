from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN

from marzban import Marzban



async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 ربات فروش Marzban فعال شد\n\n"
        "🛒 سیستم فروش به زودی آماده می‌شود."
    )



async def test_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "⏳ در حال ساخت کاربر..."
    )


    marzban = Marzban()


    result = marzban.create_user(
        username=None,
        days=30
    )


    if result:

        username = result.get(
            "username",
            "نامشخص"
        )


        await update.message.reply_text(
            f"✅ کاربر ساخته شد\n\n"
            f"👤 نام کاربر:\n"
            f"{username}\n\n"
            f"{result}"
        )

    else:

        await update.message.reply_text(
            "❌ ساخت کاربر ناموفق بود"
        )



def main():


    print("Testing Marzban...")


    marzban = Marzban()


    marzban.test()



    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )



    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "testuser",
            test_user
        )
    )



    print(
        "Bot Started ✅"
    )


    app.run_polling()



if __name__ == "__main__":

    main()
