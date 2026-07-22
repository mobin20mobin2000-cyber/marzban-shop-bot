from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN, MARZBAN_URL
from marzban import Marzban



async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 ربات فروش Marzban فعال شد\n\n"
        "🛒 سیستم فروش اشتراک آماده است."
    )



async def test_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "⏳ در حال ساخت اشتراک..."
    )


    marzban = Marzban()


    result = marzban.create_user(
        username=None,
        days=30
    )


    if result:

        username = result.get(
            "username"
        )


        sub_path = result.get(
            "subscription_url"
        )


        sub_url = (
            MARZBAN_URL.rstrip("/")
            +
            sub_path
        )


        await update.message.reply_text(
            "✅ اشتراک شما آماده شد\n\n"
            f"👤 کاربر:\n"
            f"{username}\n\n"
            "📅 مدت: ۳۰ روز\n\n"
            "🔗 لینک سابسکریپشن:\n"
            f"{sub_url}"
        )


    else:

        await update.message.reply_text(
            "❌ ساخت اشتراک ناموفق بود"
        )



def main():

    print(
        "Testing Marzban..."
    )


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
