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


from config import (
    ADMIN_ID,
    CARD_NUMBER
)


from database import (
    add_user,
    get_user_service
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


    return InlineKeyboardMarkup(
        keyboard
    )





# ==========================================================
# Start
# ==========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    add_user(
        user.id,
        user.username
    )


    text = f"""
👑 Zeus Shop VPN PRO


سلام {user.first_name} 🌹


به ربات فروش اشتراک VPN خوش آمدید.


🚀 سرعت بالا
🔒 امنیت پایدار
🌍 سرورهای قدرتمند


از منوی زیر انتخاب کنید:
"""


    await update.message.reply_text(

        text,

        reply_markup=main_keyboard()

    )





# ==========================================================
# My Service
# ==========================================================


async def my_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query


    await query.answer()


    user_id = query.from_user.id


    service = get_user_service(
        user_id
    )



    if not service:


        await query.edit_message_text(

            """
❌ شما هنوز سرویس فعالی ندارید.

برای خرید اشتراک از بخش خرید استفاده کنید.
"""
        )


        return




    text = f"""
📦 سرویس من


👤 Username:

{service['username']}


🌐 لینک اتصال:

{service['subscription_url']}


📊 حجم:

{service['volume']} GB


⏳ مدت:

{service['days']} روز


✅ وضعیت:

فعال
"""


    await query.edit_message_text(
        text
    )
    # ==========================================================
# Buy System
# Part 2
# ==========================================================


from database import (
    create_order,
    last_order
)





# ==========================================================
# Plans Keyboard
# ==========================================================


def plans_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🥉 یک ماهه | 50GB | 50,000 تومان",
                callback_data="plan_30"
            )
        ],

        [
            InlineKeyboardButton(
                "🥈 دو ماهه | 100GB | 90,000 تومان",
                callback_data="plan_60"
            )
        ],

        [
            InlineKeyboardButton(
                "🥇 سه ماهه | 200GB | 150,000 تومان",
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


    return InlineKeyboardMarkup(
        keyboard
    )





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
🛒 خرید اشتراک Zeus VPN


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


    plan = query.data



    if plan == "plan_30":

        data = {

            "name": "یک ماهه",

            "volume": 50,

            "days": 30,

            "price": 50000

        }



    elif plan == "plan_60":

        data = {

            "name": "دو ماهه",

            "volume": 100,

            "days": 60,

            "price": 90000

        }



    elif plan == "plan_90":

        data = {

            "name": "سه ماهه",

            "volume": 200,

            "days": 90,

            "price": 150000

        }


    else:

        return





    order_id = create_order(

        telegram_id=user_id,

        plan=data["name"],

        volume=data["volume"],

        days=data["days"],

        price=data["price"]

    )



    context.user_data["order_id"] = order_id





    await query.edit_message_text(

        f"""
✅ سفارش شما ثبت شد.


📦 پلن:

{data['name']}


📊 حجم:

{data['volume']}GB


⏳ مدت:

{data['days']} روز


💰 مبلغ:

{data['price']:,} تومان


لطفاً از بخش پرداخت، رسید خود را ارسال کنید.
""",

        reply_markup=InlineKeyboardMarkup([

            [

                InlineKeyboardButton(

                    "💳 پرداخت",

                    callback_data="payment"

                )

            ]

        ])

            )
    # ==========================================================
# Payment + Support + Admin
# Part 3
# ==========================================================


from database import (
    save_receipt,
    save_support_message,
    get_order,
    update_order_status,
    save_service
)


from marzban import Marzban





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
💳 پرداخت دستی Zeus VPN


شماره کارت:

{CARD_NUMBER}


بعد از پرداخت،
عکس رسید را ارسال کنید.


✅ رسید توسط مدیریت بررسی می‌شود.
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
✅ رسید دریافت شد.


بعد از تایید مدیریت،
سرویس شما ساخته می‌شود.
"""

    )



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=file_id,

        caption=f"""
📥 رسید پرداخت جدید


👤 User ID:

{user_id}


برای تایید:

/approve {user_id}


برای رد:

/reject {user_id}
"""

    )





# ==========================================================
# Support
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
🆘 پشتیبانی Zeus VPN


پیام خود را ارسال کنید.
"""

    )





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
"""

    )



    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=f"""
🆘 پیام پشتیبانی


👤 کاربر:

{user_id}


💬 پیام:

{message}
"""

    )





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
            "فرمت اشتباه است."
        )

        return





    order = get_order(
        user_id
    )



    if not order:

        await update.message.reply_text(
            "❌ سفارش پیدا نشد."
        )

        return





    marzban = Marzban()



    user = marzban.create_user(

        username=str(user_id),

        data_limit=order["volume"]

    )



    if not user:

        await update.message.reply_text(

            "❌ ساخت سرویس ناموفق بود."

        )

        return





    username = user["username"]


    link = marzban.subscription(

        username

    )





    save_service(

        telegram_id=user_id,

        username=username,

        subscription_url=link,

        volume=order["volume"],

        days=order["days"],

        order_id=order["id"]

    )





    update_order_status(

        user_id,

        "approved"

    )





    await context.bot.send_message(

        chat_id=user_id,

        text=f"""
🎉 پرداخت تایید شد.


✅ سرویس شما فعال شد.


🔐 لینک اتصال:

{link}
"""

    )



    await update.message.reply_text(

        "✅ سرویس ساخته شد."

    )





# ==========================================================
# Reject
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

لطفاً دوباره ارسال کنید.
"""

    )


    await update.message.reply_text(

        "❌ رد شد."

    )
    # ==========================================================
# Register Handlers
# Part 4
# ==========================================================


from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
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

        """
❌ دستور قابل تشخیص نیست.

از منوی ربات استفاده کنید.
"""

    )





# ==========================================================
# Register All
# ==========================================================


def register_handlers(
    application
):


    # --------------------------
    # Start
    # --------------------------

    application.add_handler(

        CommandHandler(
            "start",
            start
        )

    )



    # --------------------------
    # Admin Commands
    # --------------------------

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



    # --------------------------
    # Main Buttons
    # --------------------------


    application.add_handler(

        CallbackQueryHandler(
            buy,
            pattern="^buy$"
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



    # --------------------------
    # Plans
    # --------------------------


    application.add_handler(

        CallbackQueryHandler(
            select_plan,
            pattern="^plan_"
        )

    )



    # --------------------------
    # Receipt
    # --------------------------


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )



    # --------------------------
    # Text
    # --------------------------


    application.add_handler(

        MessageHandler(

            filters.TEXT
            &
            ~filters.COMMAND,

            text_router

        )

    )


# ==========================================================
# END handlers.py
# Zeus Shop VPN PRO
# ==========================================================
