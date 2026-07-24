# =========================
# main.py
# Zeus Shop VPN
# =========================


from telegram.ext import Application

from config import BOT_TOKEN

from handlers import register_handlers

from database import init_db



# =========================
# اجرای ربات
# =========================

def main():


    # ساخت دیتابیس و جدول‌ها

    init_db()



    # ساخت ربات

    app = Application.builder().token(

        BOT_TOKEN

    ).build()



    # ثبت Handler ها

    register_handlers(

        app

    )



    print(
        "🚀 Zeus Shop VPN Bot Started"
    )



    # اجرای ربات

    app.run_polling()



# =========================
# شروع
# =========================

if __name__ == "__main__":

    main()
