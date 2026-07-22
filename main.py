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
        "به زودی سیستم فروش اشتراک آماده می‌شود."
    )



def main():

    print("Testing Marzban...")

    marzban = Marzban()

    marzban.test()


    app = Application.builder() \
        .token(BOT_TOKEN) \
        .build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    print("Bot Started ✅")


    app.run_polling()



if __name__ == "__main__":
    main()
