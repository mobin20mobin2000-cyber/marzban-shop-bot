# =========================
# main.py
# Zeus Shop VPN
# =========================

from telegram.ext import Application

from config import BOT_TOKEN

from handlers import register_handlers

from database import init_db


def main():

    # ساخت دیتابیس
    init_db()


    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    register_handlers(app)


    print(
        "🚀 Zeus Shop VPN Started"
    )


    app.run_polling()



if __name__ == "__main__":

    main()
