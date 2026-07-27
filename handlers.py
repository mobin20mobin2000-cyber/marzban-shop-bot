# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 1/4
# ==========================================================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)



from config import (
    ADMIN_ID,
    CARD_NUMBER
)


from database import (
    add_user,
    get_user_service,
    create_order,
    last_order,
    save_receipt
)



# ==========================================================
# Main Menu
# ==========================================================


def main_menu():


    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 خرید سرویس",
                callback_data="buy"
            )
        ],


        [
            InlineKeyboardButton(
                "👤 سرویس من",
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
                "🎧 پشتیبانی",
                callback_data="support"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )





# ==========================================================
# Start Command
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

👑 Zeus Shop VPN

سلام {user.first_name} 🌹


به ربات فروش VPN خوش آمدید.


🚀 سرویس پرسرعت
🔐 امن و پایدار


از منوی زیر انتخاب کنید:

"""


    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )





# ==========================================================
# Register
# ==========================================================


def register_handlers(
    application
):


    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )
    # ==========================================================
# Buy Menu
# Part 2/4
# ==========================================================


def plans_menu():


    keyboard = [


        [
            InlineKeyboardButton(
                "📦 30 گیگ - 30 روز",
                callback_data="plan_30"
            )
        ],


        [
            InlineKeyboardButton(
                "📦 60 گیگ - 30 روز",
                callback_data="plan_60"
            )
        ],


        [
            InlineKeyboardButton(
                "📦 100 گیگ - 60 روز",
                callback_data="plan_100"
            )
        ],


        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back_home"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )





# ==========================================================
# Create Order From Plan
# ==========================================================


async def create_plan_order(
    query,
    telegram_id,
    volume,
    days,
    price
):


    order_id = create_order(

        telegram_id,

        f"{volume}GB",

        volume,

        days,

        price

    )


    await query.edit_message_text(

        f"""
✅ سفارش ساخته شد


📦 حجم:
{volume} گیگ


⏳ مدت:
{days} روز


💰 مبلغ:
{price:,} تومان


شماره سفارش:
#{order_id}


اکنون پرداخت کنید.
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
# Plan Handler
# ==========================================================


async def plan_handler(
    query
):


    telegram_id = query.from_user.id


    data = query.data



    if data == "plan_30":


        await create_plan_order(
            query,
            telegram_id,
            30,
            30,
            70000
        )



    elif data == "plan_60":


        await create_plan_order(
            query,
            telegram_id,
            60,
            30,
            120000
        )



    elif data == "plan_100":


        await create_plan_order(
            query,
            telegram_id,
            100,
            60,
            200000
            )
        # ==========================================================
# My Service
# Part 3/4
# ==========================================================


async def my_service(
    query
):


    telegram_id = query.from_user.id


    service = get_user_service(
        telegram_id
    )


    if not service:


        await query.edit_message_text(

            """
❌ شما هنوز سرویس فعالی ندارید.

برای خرید از منوی اصلی اقدام کنید.
""",

            reply_markup=main_menu()

        )

        return





    text = f"""

🌐 سرویس شما


━━━━━━━━━━━━


👤 نام کاربر:

{service['username']}


📦 حجم:

{service['volume']} GB


⏳ مدت:

{service['days']} روز


🔗 لینک اتصال:

{service['subscription_url']}


━━━━━━━━━━━━

"""


    await query.edit_message_text(

        text,

        reply_markup=main_menu()

    )





# ==========================================================
# Payment Menu
# ==========================================================


async def payment_menu(
    query
):


    order = last_order(
        query.from_user.id
    )



    if not order:


        await query.edit_message_text(

            """
❌ سفارشی پیدا نشد.

ابتدا یک سرویس خریداری کنید.
""",

            reply_markup=main_menu()

        )

        return





    text = f"""

💳 پرداخت سفارش


━━━━━━━━━━━━


🧾 شماره سفارش:

#{order['id']}


💰 مبلغ:

{order['price']:,} تومان


شماره کارت:


{CARD_NUMBER}


━━━━━━━━━━━━


بعد از پرداخت، عکس رسید را ارسال کنید.
"""


    await query.edit_message_text(
        text
    )





# ==========================================================
# Receive Receipt
# ==========================================================


async def receive_receipt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    user_id = update.effective_user.id



    if update.message.photo:


        photo = update.message.photo[-1]


        save_receipt(

            user_id,

            photo.file_id

        )



        await update.message.reply_text(

            """
✅ رسید دریافت شد


⏳ منتظر تایید مدیریت باشید.
"""

        )


    else:


        await update.message.reply_text(

            """
❌ لطفا فقط عکس رسید ارسال کنید.
"""

)
        # ==========================================================
# Admin + Buttons
# Part 4/4
# ==========================================================


from admin import admin_panel





async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    query = update.callback_query


    await query.answer()


    data = query.data





    # =====================
    # Home
    # =====================


    if data == "back_home":


        await query.edit_message_text(

            "🏠 منوی اصلی",

            reply_markup=main_menu()

        )

        return





    # =====================
    # Buy
    # =====================


    if data == "buy":


        await query.edit_message_text(

            "📦 پلن مورد نظر را انتخاب کنید:",

            reply_markup=plans_menu()

        )

        return





    # =====================
    # Plans
    # =====================


    if data.startswith(
        "plan_"
    ):


        await plan_handler(
            query
        )

        return





    # =====================
    # Service
    # =====================


    if data == "my_service":


        await my_service(
            query
        )

        return





    # =====================
    # Payment
    # =====================


    if data == "payment":


        await payment_menu(
            query
        )

        return





    # =====================
    # Support
    # =====================


    if data == "support":


        await query.edit_message_text(

            """
🎧 پشتیبانی


برای ارتباط با مدیریت پیام ارسال کنید.
"""

        )

        return





    # =====================
    # Admin
    # =====================


    if data == "admin":


        if query.from_user.id != ADMIN_ID:


            await query.edit_message_text(
                "❌ دسترسی ندارید."
            )

            return



        await query.edit_message_text(

            "👑 پنل مدیریت",

            reply_markup=admin_panel()

        )

        return







# ==========================================================
# Register More Handlers
# ==========================================================


def register_handlers(
    application
):


    application.add_handler(

        CommandHandler(
            "start",
            start
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            button_handler
        )

    )


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_receipt

        )

        )
