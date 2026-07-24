# =========================
# main.py
# Zeus Shop VPN
# =========================


from telegram.ext import Application


from config import BOT_TOKEN


from handlers import register_handlers



# =========================
# اجرای ربات
# =========================

def main():


    app = Application.builder().token(

        BOT_TOKEN

    ).build()



    # ثبت تمام هندلرها

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
