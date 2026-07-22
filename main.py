from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, ADMIN_ID, MARZBAN_URL

from order import create_order

from payment import get_payment_text

from admin import admin_buttons, create_subscription


# نگهداری سفارش‌های در انتظار
waiting_receipt = {}


def user_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 خرید اشتراک",
                callback_data="buy"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 سرویس من",
                callback_data="my_service"
            )
        ],
        [
            InlineKeyboardButton(
                "🆘 پشتیبانی",
                callback_data="support"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)



def admin_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "📋 سفارش‌ها",
                callback_data="orders"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    if user_id == ADMIN_ID:

        await update.message.reply_text(
            "👨‍💼 پنل مدیریت",
            reply_markup=admin_menu()
        )

    else:

        await update.message.reply_text(
            "🤖 ربات فروش اشتراک\n\n"
            "یک گزینه را انتخاب کنید:",
            reply_markup=user_menu()
        )



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id



    # خرید

    if query.data == "buy":


        order_id = create_order(
            user_id,
            "30 روزه"
        )


        waiting_receipt[user_id] = order_id


        await query.message.reply_text(
            get_payment_text(order_id)
        )



    # سرویس من

    elif query.data == "my_service":


        await query.message.reply_text(
            "📦 هنوز سرویسی برای شما ثبت نشده است."
        )



    # پشتیبانی

    elif query.data == "support":


        await query.message.reply_text(
            "🆘 پشتیبانی"
        )



    # تایید مدیر

    elif query.data.startswith("approve_"):


        order_id = query.data.replace(
            "approve_",
            ""
        )


        customer_id = None


        for uid, oid in waiting_receipt.items():

            if oid == order_id:

                customer_id = uid

                break



        if customer_id is None:


            await query.message.reply_text(
                "❌ کاربر سفارش پیدا نشد"
            )

            return



        result = create_subscription()



        if result:


            sub_url = (

                MARZBAN_URL.rstrip("/")

                +

                result["subscription"]

            )



            await context.bot.send_message(

                chat_id=customer_id,

                text=(

                    "✅ پرداخت شما تأیید شد\n\n"

                    f"👤 نام کاربر:\n"

                    f"{result['username']}\n\n"

                    "🔗 لینک سابسکریپشن:\n"

                    f"{sub_url}"

                )

            )



            await query.message.reply_text(

                "✅ پرداخت تأیید شد\n"

                "📩 لینک برای مشتری ارسال شد."

            )


        else:


            await query.message.reply_text(

                "❌ ساخت اشتراک ناموفق بود"

            )



    # رد پرداخت

    elif query.data.startswith("reject_"):


        await query.message.reply_text(

            "❌ پرداخت رد شد"

        )




async def receipt_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id


    if user_id not in waiting_receipt:

        return



    order_id = waiting_receipt[user_id]


    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(

            "📥 رسید پرداخت جدید\n\n"

            f"👤 کاربر:\n{user_id}\n\n"

            f"🆔 سفارش:\n{order_id}"

        ),

        reply_markup=admin_buttons(order_id)

    )



    await update.message.reply_text(

        "✅ رسید ارسال شد\n"

        "⏳ منتظر تأیید مدیر باشید."

    )




def main():


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

        CallbackQueryHandler(

            button

        )

    )



    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )



    print(

        "Bot Started ✅"

    )


    app.run_polling()



if __name__ == "__main__":

    main()
