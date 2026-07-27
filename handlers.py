# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 1/5
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
    save_receipt,
    approve_payment,
    reject_payment
)



# ==========================================================
# User Main Menu
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
        ],


        [
            InlineKeyboardButton(
                "👑 مدیریت",
                callback_data="admin"
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


سلام {user.first_name} عزیز 🌹


به بزرگترین فروشگاه سرویس VPN خوش آمدید.


━━━━━━━━━━━━━━━━━━


🚀 اینترنت سریع و پایدار

🔐 اتصال امن و مطمئن

⚡ فعال‌سازی سریع سرویس

🌍 مناسب بازی، وب‌گردی و استفاده روزمره


━━━━━━━━━━━━━━━━━━


امکانات ربات:


🛒 خرید سرویس

👤 مشاهده سرویس من

💳 پرداخت آسان

🎧 پشتیبانی


━━━━━━━━━━━━━━━━━━


✨ از منوی زیر انتخاب کنید.


💎 Zeus Shop VPN PRO

"""


    await update.message.reply_text(

        text,

        reply_markup=main_menu()

    )
    # ==========================================================
# Buy Plans
# Part 2/5
# ==========================================================



def plans_menu():


    keyboard = [


        [

            InlineKeyboardButton(

                "📦 50GB | 30 روز | 70,000 تومان",

                callback_data="plan_50"

            )

        ],


        [

            InlineKeyboardButton(

                "📦 100GB | 30 روز | 140,000 تومان",

                callback_data="plan_100"

            )

        ],


        [

            InlineKeyboardButton(

                "♾ نامحدود | 30 روز | 165,000 تومان",

                callback_data="plan_unlimited"

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
# Create Order
# ==========================================================


async def create_plan_order(

    query,

    telegram_id,

    plan,

    volume,

    days,

    price

):


    order_id = create_order(

        telegram_id,

        plan,

        volume,

        days,

        price

    )



    text = f"""

✅ سفارش شما ثبت شد


━━━━━━━━━━━━


🧾 شماره سفارش:

#{order_id}


📦 سرویس:

{plan}


📊 حجم:

{volume}


⏳ مدت:

{days} روز


💰 مبلغ:

{price:,} تومان


━━━━━━━━━━━━


برای پرداخت روی دکمه زیر بزنید.

"""



    await query.edit_message_text(

        text,

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "💳 پرداخت",

                        callback_data="payment"

                    )

                ],


                [

                    InlineKeyboardButton(

                        "🔙 بازگشت",

                        callback_data="back_home"

                    )

                ]

            ]

        )

    )







# ==========================================================
# Plan Handler
# ==========================================================


async def plan_handler(

    query

):


    user_id = query.from_user.id


    data = query.data




    if data == "plan_50":


        await create_plan_order(

            query,

            user_id,

            "50GB",

            "50GB",

            30,

            70000

        )




    elif data == "plan_100":


        await create_plan_order(

            query,

            user_id,

            "100GB",

            "100GB",

            30,

            140000

        )




    elif data == "plan_unlimited":


        await create_plan_order(

            query,

            user_id,

            "نامحدود",

            "Unlimited",

            30,

            165000

        )
        # ==========================================================
# My Service
# Part 3/5
# ==========================================================


async def my_service(
    query
):


    user_id = query.from_user.id



    service = get_user_service(

        user_id

    )



    if not service:


        await query.edit_message_text(

            """
❌ سرویس فعالی ندارید.


برای خرید سرویس از بخش خرید اقدام کنید.
""",

            reply_markup=main_menu()

        )

        return





    text = f"""

🌐 سرویس فعال شما


━━━━━━━━━━━━


👤 کاربر:

{service['username']}


📦 حجم:

{service['volume']}


⏳ مدت:

{service['days']} روز


📅 انقضا:

{service['expire_date']}


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
❌ سفارش پیدا نشد.


ابتدا سرویس خریداری کنید.
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


🏦 شماره کارت:


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


    user = update.effective_user




    if not update.message.photo:


        await update.message.reply_text(

            "❌ لطفا فقط عکس رسید ارسال کنید."

        )

        return





    photo = update.message.photo[-1]




    save_receipt(

        user.id,

        photo.file_id

    )





    await update.message.reply_text(

        """
✅ رسید شما دریافت شد.


⏳ منتظر تایید مدیریت باشید.
"""

    )





    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,


        caption=f"""

💳 رسید پرداخت جدید


━━━━━━━━━━━━


👤 کاربر:

{user.first_name}


🆔 آیدی:

{user.id}


━━━━━━━━━━━━


بررسی پرداخت:

""",


        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "✅ تایید پرداخت",

                        callback_data=f"approve_{user.id}"

                    )

                ],


                [

                    InlineKeyboardButton(

                        "❌ رد پرداخت",

                        callback_data=f"reject_{user.id}"

                    )

                ]

            ]

        )

    )
    # ==========================================================
# Admin Panel
# Part 4/5
# ==========================================================


def admin_menu():


    keyboard = [


        [

            InlineKeyboardButton(

                "📊 آمار ربات",

                callback_data="admin_stats"

            )

        ],


        [

            InlineKeyboardButton(

                "💳 رسیدهای پرداخت",

                callback_data="admin_receipts"

            )

        ],


        [

            InlineKeyboardButton(

                "🛒 سفارش‌ها",

                callback_data="admin_orders"

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
# Admin Stats
# ==========================================================


async def admin_stats(

    query

):


    from database import get_stats



    stats = get_stats()



    text = f"""

👑 پنل مدیریت Zeus


━━━━━━━━━━━━


👤 کاربران:

{stats['users']}


🆕 امروز:

{stats['today_users']}


🛒 فروش:

{stats['sales']}


🌐 سرویس‌ها:

{stats['subscriptions']}


💰 درآمد:

{stats['income']:,}


⏳ در انتظار:

{stats['pending']}


━━━━━━━━━━━━

"""



    await query.edit_message_text(

        text,

        reply_markup=admin_menu()

    )







# ==========================================================
# Approve / Reject Receipt
# ==========================================================


async def receipt_action(

    query,

    context

):


    data = query.data



    if data.startswith("approve_"):


        user_id = int(

            data.split("_")[1]

        )



        await context.bot.send_message(

            chat_id=user_id,

            text="""

✅ پرداخت شما تایید شد.


⏳ سرویس شما در حال آماده‌سازی است.

"""

        )



        await query.edit_message_caption(

            caption="""

✅ پرداخت تایید شد


کاربر مطلع شد.

"""

        )


        return






    if data.startswith("reject_"):


        user_id = int(

            data.split("_")[1]

        )



        await context.bot.send_message(

            chat_id=user_id,

            text="""

❌ پرداخت شما رد شد.


لطفا با پشتیبانی تماس بگیرید.

"""

        )



        await query.edit_message_caption(

            caption="""

❌ پرداخت رد شد

"""

        )


        return
        # ==========================================================
# Button Handler
# Part 5/5
# ==========================================================


async def button_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data





    # =========================
    # Back Home
    # =========================


    if data == "back_home":


        await query.edit_message_text(

            "🏠 منوی اصلی",

            reply_markup=main_menu()

        )

        return





    # =========================
    # Buy
    # =========================


    if data == "buy":


        await query.edit_message_text(

            "📦 پلن مورد نظر را انتخاب کنید:",

            reply_markup=plans_menu()

        )

        return





    # =========================
    # Plans
    # =========================


    if data.startswith("plan_"):


        await plan_handler(

            query

        )

        return






    # =========================
    # My Service
    # =========================


    if data == "my_service":


        await my_service(

            query

        )

        return






    # =========================
    # Payment
    # =========================


    if data == "payment":


        await payment_menu(

            query

        )

        return






    # =========================
    # Admin Open
    # =========================


    if data == "admin":


        if query.from_user.id != ADMIN_ID:


            await query.edit_message_text(

                "❌ شما دسترسی مدیریت ندارید."

            )

            return



        await query.edit_message_text(

            "👑 پنل مدیریت",

            reply_markup=admin_menu()

        )

        return





    # =========================
    # Admin Stats
    # =========================


    if data == "admin_stats":


        if query.from_user.id != ADMIN_ID:

            return


        await admin_stats(

            query

        )

        return





    # =========================
    # Receipt Approve / Reject
    # =========================


    if data.startswith("approve_") or data.startswith("reject_"):


        if query.from_user.id != ADMIN_ID:

            return



        await receipt_action(

            query,

            context

        )

        return






    # =========================
    # Support
    # =========================


    if data == "support":


        await query.edit_message_text(

            """
🎧 پشتیبانی


پیام خود را ارسال کنید.
"""

        )

        return







# ==========================================================
# Register Handlers
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
