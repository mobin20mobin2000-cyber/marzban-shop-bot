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

    if not BOT_TOKEN:

        print(
            "❌ BOT_TOKEN تنظیم نشده"
        )

        return



    # ساخت دیتابیس

    init_db()



    # ساخت اپلیکیشن تلگرام

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
# شروع برنامه
# =========================

if __name__ == "__main__":

    main()
