# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 1
# ==========================================================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes
)


from database import (
    add_user
)


# ==========================================================
# Main Keyboard
# ==========================================================


def main_keyboard():

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
                "💳 پرداخت",
                callback_data="payment"
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



# ==========================================================
# Start Command
# ==========================================================


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    # ذخیره کاربر در دیتابیس

    add_user(

        telegram_id=user.id,

        username=user.username

    )


    text = f"""

👑 Zeus Shop VPN PRO


سلام {user.first_name} عزیز 🌹


به ربات فروش اشتراک VPN خوش آمدید.


🚀 اتصال سریع
🔒 امن و پایدار
🌍 سرورهای قدرتمند


از منوی زیر انتخاب کنید:
"""


    await update.message.reply_text(

        text,

        reply_markup=main_keyboard()

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 2
# Buy System
# ==========================================================


from database import (
    create_order
)



# ==========================================================
# Plans Keyboard
# ==========================================================


def plans_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🥉 یک ماهه | 50GB",
                callback_data="plan_30"
            )
        ],

        [
            InlineKeyboardButton(
                "🥈 دو ماهه | 100GB",
                callback_data="plan_60"
            )
        ],

        [
            InlineKeyboardButton(
                "🥇 سه ماهه | 200GB",
                callback_data="plan_90"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)



# ==========================================================
# Buy Button
# ==========================================================


async def buy(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.edit_message_text(

        """
🛒 خرید اشتراک Zeus VPN PRO


پلن مورد نظر را انتخاب کنید:
""",

        reply_markup=plans_keyboard()

    )



# ==========================================================
# Select Plan
# ==========================================================


async def select_plan(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    plan_id = query.data



    if plan_id == "plan_30":

        plan_name = "یک ماهه"

        volume = 50

        days = 30

        price = 50000



    elif plan_id == "plan_60":

        plan_name = "دو ماهه"

        volume = 100

        days = 60

        price = 90000



    elif plan_id == "plan_90":

        plan_name = "سه ماهه"

        volume = 200

        days = 90

        price = 130000



    else:

        return



    order_id = create_order(

        telegram_id=user_id,

        plan=plan_name,

        volume=volume,

        days=days,

        price=price

    )


    context.user_data["order_id"] = order_id



    await query.edit_message_text(

        f"""

🧾 فاکتور خرید


📦 پلن:

{plan_name}


📊 حجم:

{volume} GB


⏳ مدت:

{days} روز


💰 مبلغ:

{price:,} تومان


🧾 شماره سفارش:

{order_id}


برای پرداخت از بخش 💳 پرداخت استفاده کنید.
"""

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 3
# Payment + Support
# ==========================================================


from config import (
    ADMIN_ID,
    CARD_NUMBER
)


from database import (
    save_receipt,
    save_support_message
)



# ==========================================================
# Payment
# ==========================================================


async def payment(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.edit_message_text(

        f"""

💳 پرداخت دستی


شماره کارت:

{CARD_NUMBER}


بعد از پرداخت، عکس رسید را ارسال کنید.


✅ رسید شما توسط ادمین بررسی می‌شود.
"""

    )



# ==========================================================
# Receipt Photo
# ==========================================================


async def receipt_photo(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id


    photo = update.message.photo[-1]


    file_id = photo.file_id



    save_receipt(

        user_id,

        file_id

    )



    await update.message.reply_text(

        """

✅ رسید شما دریافت شد.


پس از بررسی ادمین،
سرویس فعال می‌شود.

"""

    )



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=file_id,

        caption=f"""

📥 رسید پرداخت جدید


👤 کاربر:

{user_id}


برای بررسی سفارش اقدام کنید.

"""

    )



# ==========================================================
# Support Button
# ==========================================================


async def support(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    context.user_data["waiting_support"] = True



    await query.edit_message_text(

        """

🆘 پشتیبانی Zeus VPN PRO


پیام خود را ارسال کنید.

"""

    )



# ==========================================================
# Support Message
# ==========================================================


async def support_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if not context.user_data.get(
        "waiting_support"
    ):

        return



    user_id = update.message.from_user.id


    message = update.message.text



    save_support_message(

        user_id,

        message

    )



    context.user_data["waiting_support"] = False



    await update.message.reply_text(

        """

✅ پیام شما ارسال شد.


منتظر پاسخ پشتیبانی باشید.

"""

    )



    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=f"""

🆘 پیام پشتیبانی جدید


👤 کاربر:

{user_id}


💬 پیام:

{message}

"""

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 4
# Admin + Marzban + Register
# ==========================================================


from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)


from database import (
    get_order,
    update_order_status,
    save_subscription
)


from marzban import Marzban



# ==========================================================
# Admin Approve
# ==========================================================


async def approve(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if update.effective_user.id != ADMIN_ID:

        return



    try:

        user_id = int(
            context.args[0]
        )

    except:

        await update.message.reply_text(
            "فرمت صحیح نیست."
        )

        return



    order = get_order(user_id)



    if not order:

        await update.message.reply_text(
            "❌ سفارش پیدا نشد."
        )

        return



    marzban = Marzban()



    if not marzban.login():

        await update.message.reply_text(
            "❌ اتصال به Marzban ناموفق بود."
        )

        return



    user = marzban.create_user(

        username=str(user_id),

        data_limit=order["volume"] * 1024 * 1024 * 1024

    )



    if not user:

        await update.message.reply_text(
            "❌ ساخت کاربر Marzban انجام نشد."
        )

        return



    username = user.get(
        "username"
    )



    subscription = marzban.subscription(
        username
    )



    save_subscription(

        telegram_id=user_id,

        order_id=order["id"],

        marzban_username=username,

        subscription_url=subscription

    )



    update_order_status(

        order["id"],

        "approved"

    )



    await context.bot.send_message(

        chat_id=user_id,

        text=f"""

🎉 پرداخت شما تایید شد.


✅ سرویس شما فعال شد.


👤 Username:

{username}


🔗 لینک اتصال:

{subscription}


ممنون از خرید شما 🌹

"""

    )



    await update.message.reply_text(
        "✅ سرویس ساخته شد."
    )



# ==========================================================
# Admin Reject
# ==========================================================


async def reject(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if update.effective_user.id != ADMIN_ID:

        return



    try:

        user_id = int(
            context.args[0]
        )

    except:

        return



    update_order_status(

        user_id,

        "rejected"

    )



    await context.bot.send_message(

        chat_id=user_id,

        text="""

❌ پرداخت رد شد.


لطفاً دوباره بررسی و ارسال کنید.

"""

    )



    await update.message.reply_text(
        "❌ پرداخت رد شد."
    )



# ==========================================================
# Text Router
# ==========================================================


async def text_router(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if context.user_data.get(
        "waiting_support"
    ):

        await support_message(
            update,
            context
        )

        return



    await update.message.reply_text(

        "❌ از منوی ربات استفاده کنید."

    )



# ==========================================================
# Register Handlers
# ==========================================================


def register_handlers(application):


    application.add_handler(

        CommandHandler(
            "start",
            start
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            buy,
            pattern="^buy$"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            select_plan,
            pattern="^plan_"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            my_service,
            pattern="^my_service$"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            payment,
            pattern="^payment$"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            support,
            pattern="^support$"
        )

    )


    application.add_handler(

        MessageHandler(
            filters.PHOTO,
            receipt_photo
        )

    )


    application.add_handler(

        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_router
        )

    )


    application.add_handler(

        CommandHandler(
            "approve",
            approve
        )

    )


    application.add_handler(

        CommandHandler(
            "reject",
            reject
        )

    )
