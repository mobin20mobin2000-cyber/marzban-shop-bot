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


from config import (
    BOT_TOKEN,
    ADMIN_ID
)


from order import create_order

from payment import get_payment_text

from admin import (
    admin_buttons,
    create_subscription
)

from storage import (
    save_service,
    get_service,
    save_order,
    get_order,
    delete_order
)

from admin_panel import admin_panel

from plans import (
    PLANS,
    get_plan
)



# ذخیره سفارش موقت نیست
# سفارش ها در storage ذخیره می شوند



# =========================
# منوی کاربر
# =========================

def user_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 🛒 خرید اشتراک",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "🔵 📦 سرویس من",
                callback_data="my_service"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 🆘 پشتیبانی",
                callback_data="support"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)





# =========================
# منوی پلن ها
# =========================

def plans_keyboard():

    keyboard = []


    for key, plan in PLANS.items():

        keyboard.append(

            [

                InlineKeyboardButton(

                    text=(
                        f"📦 {plan['name']} "
                        f"| 💰 {plan['price']:,} تومان"
                    ),

                    callback_data=f"plan_{key}"

                )

            ]

        )


    return InlineKeyboardMarkup(keyboard)





# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    if user_id == ADMIN_ID:


        await update.message.reply_text(

            "👨‍💼 پنل مدیریت",

            reply_markup=admin_panel()

        )


    else:


        await update.message.reply_text(

            "🤖 ربات فروش اشتراک\n\n"
            "یکی از گزینه‌ها را انتخاب کنید:",

            reply_markup=user_menu()

        )





# =========================
# دکمه های اصلی
# =========================

async def button(
    update: Update,
    context:
    # =========================
# نمایش سرویس من
# =========================

async def show_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    user_id = query.from_user.id


    service = get_service(user_id)


    if service:


        await query.message.reply_text(

            "📦 سرویس شما:\n\n"

            f"👤 نام کاربری:\n"
            f"{service['username']}\n\n"

            "🔗 لینک اشتراک:\n"

            f"{service['subscription']}"

        )


    else:


        await query.message.reply_text(

            "❌ هنوز سرویسی برای شما ثبت نشده."

        )





# =========================
# پشتیبانی
# =========================

async def show_support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query


    await query.message.reply_text(

        "🆘 پشتیبانی\n\n"
        "پیام خود را ارسال کنید."

    )





# =========================
# دریافت رسید پرداخت
# =========================

async def receipt_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id


    order = get_order(user_id)


    if not order:


        await update.message.reply_text(

            "❌ ابتدا یک سفارش ایجاد کنید."

        )

        return



    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(

            "📥 رسید پرداخت جدید\n\n"

            f"👤 کاربر:\n{user_id}\n\n"

            f"🆔 سفارش:\n{order['order_id']}\n\n"

            f"📦 پلن:\n{order['plan']['name']}"

        ),

        reply_markup=admin_buttons(

            order["order_id"]

        )

    )



    await update.message.reply_text(

        "✅ رسید ارسال شد.\n"
        "⏳ منتظر تایید مدیریت باشید."

    )





# =========================
# تایید پرداخت
# =========================

async def approve_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    order_id = query.data.replace(

        "approve_",

        ""

    )



    order = get_order(order_id)



    if not order:


        await query.message.reply_text(

            "❌ سفارش پیدا نشد"

        )

        return




    user_id = order["user_id"]

    plan = order["plan"]



    result = create_subscription(

        plan["volume"]

    )



    if not result:


        await query.message.reply_text(

            "❌ خطا در ساخت سرویس"

        )

        return




    save_service(

        user_id,

        result["username"],

        result["subscription"]

    )



    delete_order(

        order_id

    )



    await context.bot.send_message(

        chat_id=user_id,

        text=(

            "✅ پرداخت تایید شد\n\n"

            f"👤 نام کاربری:\n"
            f"{result['username']}\n\n"

            "🔗 لینک اشتراک:\n"

            f"{result['subscription']}"

        )

    )


    await query.message.reply_text(

        "✅ سرویس ساخته شد
      # =========================
# رد پرداخت
# =========================

async def reject_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    order_id = query.data.replace(

        "reject_",

        ""

    )


    delete_order(

        order_id

    )


    await query.message.reply_text(

        "❌ پرداخت رد شد."

    )





# =========================
# اجرای ربات
# =========================

def main():


    app = Application.builder().token(

        BOT_TOKEN

    ).build()



    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            button,

            pattern="^(buy|plan_)"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_service,

            pattern="^my_service$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_support,

            pattern="^support$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

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
