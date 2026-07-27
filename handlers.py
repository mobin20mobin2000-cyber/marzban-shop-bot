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
    create_order,
    get_user_service,
    save_receipt,
    save_support_message,
    last_order
)


# ==========================================================
# متن خوش آمدگویی
# ==========================================================


WELCOME_TEXT = """

👑 به Zeus Shop VPN PRO خوش آمدید

━━━━━━━━━━━━━━

🚀 اینترنت پرسرعت و پایدار
🌍 سرورهای قدرتمند
🔐 اتصال امن و مطمئن

━━━━━━━━━━━━━━

یکی از گزینه‌ها را انتخاب کنید 👇

"""


# ==========================================================
# منوی اصلی کاربر
# ==========================================================


def user_menu():

    keyboard = [

        [

            InlineKeyboardButton(
                "🛒 خرید سرویس",
                callback_data="buy_service"
            )

        ],

        [

            InlineKeyboardButton(
                "🌐 سرویس من",
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
                "📞 پشتیبانی",
                callback_data="support"
            )

        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# دستور Start
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


    await update.message.reply_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )



# ==========================================================
# پنل خرید
# ==========================================================


def plans_menu():


    keyboard = [

        [

            InlineKeyboardButton(
                "📦 50 گیگ - 30 روز",
                callback_data="plan
                # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 2/4
# ==========================================================


from database import (
    create_order,
    last_order,
    save_receipt,
    get_user_service
)



# ==========================================================
# انتخاب پلن
# ==========================================================


async def select_plan(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    data = query.data


    plans = {

        "plan_50": {
            "name": "50 گیگ 30 روزه",
            "volume": 50,
            "days": 30,
            "price": 50000
        },


        "plan_100": {
            "name": "100 گیگ 30 روزه",
            "volume": 100,
            "days": 30,
            "price": 90000
        },


        "plan_200": {
            "name": "200 گیگ 60 روزه",
            "volume": 200,
            "days": 60,
            "price": 160000
        }

    }



    plan = plans.get(data)



    if not plan:

        return



    user_id = query.from_user.id



    order_id = create_order(

        user_id,

        plan["name"],

        plan["volume"],

        plan["days"],

        plan["price"]

    )



    context.user_data["order_id"] = order_id



    text = f"""

✅ سفارش شما ثبت شد

━━━━━━━━━━━━

📦 پلن:
{plan['name']}

💾 حجم:
{plan['volume']} گیگ

⏳ مدت:
{plan['days']} روز

💰 مبلغ:
{plan['price']:,} تومان

🆔 شماره سفارش:
{order_id}

━━━━━━━━━━━━

لطفاً مبلغ را به کارت زیر واریز کنید:

💳 {CARD_NUMBER}

بعد از پرداخت، رسید را ارسال کنید.

"""



    keyboard = [

        [

            InlineKeyboardButton(
                "📤 ارسال رسید",
                callback_data="send_receipt"
            )

        ],


        [

            InlineKeyboardButton(
                "🔙 برگشت",
                callback_data="back_home"
            )

        ]

    ]



    await query.edit_message_text(

        text,

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )

    )





# ==========================================================
# درخواست ارسال رسید
# ==========================================================


async def request_receipt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    context.user_data["waiting_receipt"] = True



    await query.edit_message_text(

        """

📤 لطفاً عکس رسید پرداخت را ارسال کنید.

بعد از بررسی، سرویس شما فعال خواهد شد.

"""

    )





# ==========================================================
# دریافت رسید عکس
# ==========================================================


async def receive_receipt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not context.user_data.get(
        "waiting_receipt"
    ):

        return



    user_id = update.effective_user.id



    photo = update.message.photo[-1]


    file_id = photo.file_id



    save_receipt(

        user_id,

        file_id

    )



    context.user_data["waiting_receipt"] = False



    await update.message.reply_text(

        """

✅ رسید شما دریافت شد

⏳ در انتظار بررسی مدیریت هستید.

"""

    )





# ==========================================================
# سرویس من
# ==========================================================


async def my_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    service = get_user_service(

        query.from_user.id

    )



    if not service:


        await query.edit_message_text(

            """

❌ هنوز سرویسی برای شما ثبت نشده است.

"""

        )

        return




    text = f"""

🌐 سرویس شما

━━━━━━━━━━━━

👤 نام:
{service['username']}

🔗 لینک اتصال:

{service['subscription_url']}

💾 حجم:
{service['volume']} گیگ

⏳ مدت:
{service['days']} روز

━━━━━━━━━━━━

"""



    await query.edit_message_text(

        text

)
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 3/4
# ==========================================================


from database import (
    pending_receipts,
    update_receipt_status,
    get_order_by_id,
    approve_payment,
    reject_payment,
    save_service
)


from admin import (
    admin_home,
    admin_dashboard,
    users_menu,
    orders_menu,
    payments_menu,
    services_menu,
    panels_menu,
    settings_menu,
    coupon_menu,
    broadcast_menu,
    create_subscription
)



# ==========================================================
# پنل ادمین
# ==========================================================


async def admin_panel_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    if user_id != ADMIN_ID:

        return



    await update.message.reply_text(

        "👑 پنل مدیریت Zeus Shop VPN",

        reply_markup=admin_home()

    )





# ==========================================================
# کنترل دکمه‌های ادمین
# ==========================================================


async def admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    if user_id != ADMIN_ID:

        return



    data = query.data



    if data == "admin_stats":


        text, keyboard = admin_dashboard()


        await query.edit_message_text(

            text,

            reply_markup=keyboard

        )




    elif data == "admin_users":


        await query.edit_message_text(

            "👥 مدیریت کاربران",

            reply_markup=users_menu()

        )




    elif data == "admin_orders":


        await query.edit_message_text(

            "📋 مدیریت سفارش‌ها",

            reply_markup=orders_menu()

        )




    elif data == "admin_payments":


        await query.edit_message_text(

            "💳 مدیریت پرداخت‌ها",

            reply_markup=payments_menu()

        )




    elif data == "admin_services":


        await query.edit_message_text(

            "🌐 مدیریت سرویس‌ها",

            reply_markup=services_menu()

        )




    elif data == "admin_panels":


        await query.edit_message_text(

            "🖥 مدیریت پنل‌ها",

            reply_markup=panels_menu()

        )




    elif data == "coupon_menu":


        await query.edit_message_text(

            "🎟 کد تخفیف",

            reply_markup=coupon_menu()

        )




    elif data == "broadcast":


        await query.edit_message_text(

            "📢 پیام همگانی",

            reply_markup=broadcast_menu()

        )




    elif data == "settings":


        await query.edit_message_text(

            "⚙️ تنظیمات",

            reply_markup=settings_menu()

        )





    elif data == "admin_back":


        await query.edit_message_text(

            "👑 پنل مدیریت",

            reply_markup=admin_home()

        )





# ==========================================================
# لیست رسیدهای منتظر
# ==========================================================


async def show_pending_payments(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    receipts = pending_receipts()



    if not receipts:


        await query.edit_message_text(

            "✅ پرداخت منتظری وجود ندارد."

        )

        return




    keyboard = []



    text = "💳 پرداخت‌های منتظر:\n\n"



    for receipt in receipts:


        text += f"""

🆔 کاربر:
{receipt['telegram_id']}

"""

        keyboard.append(

            [

                InlineKeyboardButton(

                    f"✅ تایید {receipt['telegram_id']}",

                    callback_data=f"approve_{receipt['telegram_id']}"

                )

            ]

        )



    await query.edit_message_text(

        text,

        reply_markup=InlineKeyboardMarkup(keyboard)

    )





# ==========================================================
# تایید پرداخت و ساخت سرویس
# ==========================================================


async def approve_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return



    telegram_id = int(

        query.data.split("_")[1]

    )



    order = last_order(

        telegram_id

    )



    if not order:


        await query.edit_message_text(

            "❌ سفارش پیدا نشد."

        )

        return




    approve_payment(

        order["id"]

    )



    service = create_subscription(

        order["volume"]

    )



    if service:


        save_service(

            telegram_id,

            order["id"],

            service["username"],

            service["subscription"],

            order["volume"],

            order["days"]

        )



    await query.edit_message_text(

        "✅ پرداخت تایید شد و سرویس ساخته شد."

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 4/4
# ==========================================================


# ==========================================================
# پشتیبانی
# ==========================================================


async def support_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    context.user_data["support"] = True



    await query.edit_message_text(

        """

📞 پشتیبانی

لطفاً پیام خود را ارسال کنید.

"""

    )





async def receive_support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get(
        "support"
    ):

        return



    user_id = update.effective_user.id


    message = update.message.text



    save_support_message(

        user_id,

        message

    )



    context.user_data["support"] = False



    await update.message.reply_text(

        """

✅ پیام شما ارسال شد.

مدیریت در اولین فرصت پاسخ می‌دهد.

"""

    )





# ==========================================================
# برگشت به خانه
# ==========================================================


async def back_home(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query


    await query.answer()



    await query.edit_message_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )





# ==========================================================
# ثبت Handler ها
# ==========================================================


def register_handlers(
    application
):


    # Start

    application.add_handler(

        CommandHandler(
            "start",
            start
        )

    )



    # Admin

    application.add_handler(

        CommandHandler(
            "admin",
            admin_panel_handler
        )

    )



    # Callback ها


    application.add_handler(

        CallbackQueryHandler(
            show_plans,
            pattern="^buy_service$"
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
            request_receipt,
            pattern="^send_receipt$"
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
            support_handler,
            pattern="^support$"
        )

    )



    application.add_handler(

        CallbackQueryHandler(
            back_home,
            pattern="^back_home$"
        )

    )



    # Admin callbacks


    application.add_handler(

        CallbackQueryHandler(
            admin_callback,
            pattern="^admin_|^settings$|^coupon_menu$|^broadcast$"
        )

    )



    application.add_handler(

        CallbackQueryHandler(
            show_pending_payments,
            pattern="^pending_payments$"
        )

    )



    application.add_handler(

        CallbackQueryHandler(
            approve_handler,
            pattern="^approve_"
        )

    )



    # عکس رسید

    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_receipt

        )

    )



    # پیام پشتیبانی

    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            receive_support

        )

    )



# ==========================================================
# END handlers.py
# Zeus Shop VPN PRO
# ==========================================================
