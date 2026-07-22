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

from storage import save_service, get_service

from admin_panel import admin_panel

from plans import PLANS, get_plan



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



def plans_keyboard():

    keyboard = []

    for key, plan in PLANS.items():

        keyboard.append(

            [

                InlineKeyboardButton(

                    f"📦 {plan['name']} - {plan['price']} تومان",

                    callback_data=f"plan_{key}"

                )

            ]

        )

    return InlineKeyboardMarkup(keyboard)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    if user_id == ADMIN_ID:

        await update.message.reply_text(

            "👨‍💼 پنل مدیریت",

            reply_markup=admin_panel()

        )

    else:

        await update.message.reply_text(

            "🤖 ربات فروش اشتراک\n\n"
            "انتخاب کنید:",

            reply_markup=user_menu()

        )





async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id



    # خرید

    if query.data == "buy":


        await query.message.reply_text(

            "📦 حجم مورد نظر را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )



    # انتخاب حجم

    elif query.data.startswith("plan_"):


        plan_id = query.data.replace(

            "plan_",

            ""

        )


        plan = get_plan(plan_id)


        if not plan:

            return



        order_id = create_order(

            user_id,

            plan["name"]

        )



        waiting_receipt[user_id] = {


            "order_id": order_id,


            "plan": plan

        }



        await query.message.reply_text(

            get_payment_text(order_id)

            +

            "\n\n📦 پلن انتخابی: "

            +

            plan["name"]

            +

            "\n💰 مبلغ: "

            +

            plan["price"]

            +

            " تومان"

        )





    # سرویس من

    elif query.data == "my_service":


        service = get_service(user_id)


        if service:


            await query.message.reply_text(

                "📦 سرویس شما:\n\n"

                f"👤 {service['username']}\n\n"

                "🔗 Subscription:\n"

                f"{service['subscription']}"

            )


        else:


            await query.message.reply_text(

                "❌ سرویسی پیدا نشد."

            )





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



        customer = None



        for uid, data in waiting_receipt.items():

            if data["order_id"] == order_id:

                customer = uid

                break



        if customer is None:


            await query.message.reply_text(

                "❌ سفارش پیدا نشد"

            )

            return




        volume = waiting_receipt[customer]["plan"]["volume"]



        result = create_subscription(

            volume

        )



        if result:


            sub_url = (

                MARZBAN_URL.rstrip("/")

                +

                result["subscription"]

            )



            save_service(

                customer,

                result["username"],

                sub_url

            )



            await context.bot.send_message(

                chat_id=customer,

                text=(

                    "✅ پرداخت تأیید شد\n\n"

                    "👤 نام کاربر:\n"

                    f"{result['username']}\n\n"

                    "🔗 لینک اشتراک:\n"

                    f"{sub_url}"

                )

            )



            await query.message.reply_text(

                "✅ سرویس ساخته شد و ارسال گردید."

            )


        else:


            await query.message.reply_text(

                "❌ خطا در ساخت سرویس"

            )





    elif query.data.startswith("reject_"):


        await query.message.reply_text(

            "❌ پرداخت رد شد"

        )






async def receipt_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):


    user_id = update.message.from_user.id


    if user_id not in waiting_receipt:

        return



    data = waiting_receipt[user_id]



    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(

            "📥 رسید پرداخت جدید\n\n"

            f"👤 کاربر: {user_id}\n"

            f"🆔 سفارش: {data['order_id']}\n"

            f"📦 پلن: {data['plan']['name']}"

        ),

        reply_markup=admin_buttons(data["order_id"])

    )



    await update.message.reply_text(

        "✅ رسید ارسال شد\n"

        "⏳ منتظر تأیید باشید."

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
