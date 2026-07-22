# =========================
# main.py
# Zeus Shop VPN
# =========================


import logging


from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


from config import (
    BOT_TOKEN
)


from handlers import (
    start,
    button,
    show_service,
    show_support,
    receipt_photo,
    approve_payment,
    reject_payment
)



# =========================
# تنظیمات لاگ
# =========================

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

    level=logging.INFO

)


logger = logging.getLogger(__name__)
# =========================
# ساخت ربات
# =========================

def build_app():

    app = Application.builder().token(

        BOT_TOKEN

    ).build()



    # =====================
    # دستور start
    # =====================

    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    return app
    # =========================
# ثبت دکمه ها
# =========================


def register_callback_handlers(app):


    # خرید و انتخاب پلن

    app.add_handler(

        CallbackQueryHandler(

            button,

            pattern="^(buy|plan_)"

        )

    )



    # سرویس من

    app.add_handler(

        CallbackQueryHandler(

            show_service,

            pattern="^my_service$"

        )

    )



    # پشتیبانی

    app.add_handler(

        CallbackQueryHandler(

            show_support,

            pattern="^support$"

        )

    )



    # تایید پرداخت ادمین

    app.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )



    # رد پرداخت ادمین

    app.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

        )

    )
    # =========================
# ثبت Message Handler
# =========================


def register_message_handlers(app):


    # دریافت عکس رسید پرداخت

    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )





# =========================
# مدیریت خطا
# =========================

async def error_handler(
    update,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(

        "Exception while handling update:",

        exc_info=context.error

    )
    # =========================
# اجرای ربات
# =========================

def main():


    app = build_app()



    register_callback_handlers(

        app

    )



    register_message_handlers(

        app

    )



    app.add_error_handler(

        error_handler

    )



    print(

        "🤖 Zeus Shop VPN Started ✅"

    )



    app.run_polling(

        drop_pending_updates=True

    )





# =========================
# Start
# =========================

if __name__ == "__main__":

    main()
