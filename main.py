# ==========================================================
# Zeus Shop VPN PRO
# main.py
# ==========================================================


from telegram.ext import (
    Application
)


from config import BOT_TOKEN

from database import (
    init_db,
    test_database
)


from handlers import (
    register_handlers
)



# ==========================================================
# بعد از شروع برنامه
# ==========================================================

async def post_init(
    application
):

    print(
        "✅ Telegram Connected"
    )



# ==========================================================
# ساخت برنامه
# ==========================================================

def build_application():


    application = (

        Application.builder()

        .token(
            BOT_TOKEN
        )

        .post_init(
            post_init
        )

        .build()

    )


    register_handlers(
        application
    )


    return application




# ==========================================================
# اجرای اصلی
# ==========================================================

def main():


    print(
        "=" * 50
    )

    print(
        "🚀 Zeus Shop VPN PRO"
    )

    print(
        "=" * 50
    )



    if not BOT_TOKEN:


        print(
            "❌ BOT_TOKEN تنظیم نشده است"
        )

        return




    try:


        print(
            "📂 Checking Database..."
        )


        init_db()



        if test_database():


            print(
                "✅ Database Connected"
            )

        else:


            print(
                "❌ Database Error"
            )

            return





        print(
            "🤖 Loading Telegram Bot..."
        )


        application = build_application()



        print(
            "✅ Bot Started"
        )


        print(
            "⏳ Waiting for messages..."
        )



        application.run_polling()



    except KeyboardInterrupt:


        print(
            "🛑 Bot stopped"
        )



    except Exception as error:


        print(
            "❌ Fatal Error:",
            error
        )



# ==========================================================
# Start
# ==========================================================

if __name__ == "__main__":

    main()
