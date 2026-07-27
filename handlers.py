# ==========================================================
# Zeus Shop VPN PRO CLEAN
# handlers.py
# Part 1/10
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
    last_order,
    save_receipt,
    save_service,
    get_user_service,
    get_stats,
    update_order_status,
    get_pending_orders
)


from marzban import Marzban







# ==========================================================
# Style
# ==========================================================


HEADER = """
━━━━━━━━━━━━━━
👑 Zeus Shop VPN
━━━━━━━━━━━━━━
"""









# ==========================================================
# Main Menu
# ==========================================================


def main_menu(user_id=None):


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
                "🎁 کد تخفیف",
                callback_data="discount"
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
                "ℹ️ راهنما",
                callback_data="help"
            )

        ]

    ]



    if user_id == ADMIN_ID:


        keyboard.append(

            [

                InlineKeyboardButton(
                    "👑 مدیریت",
                    callback_data="admin"
                )

            ]

        )



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
{HEADER}

سلام {user.first_name} عزیز 🌹


به ربات رسمی Zeus Shop VPN خوش آمدید 🚀


━━━━━━━━━━━━━━

⚡ فعالسازی سریع
🌍 سرورهای پرسرعت
🔐 اتصال امن
🎧 پشتیبانی فعال

━━━━━━━━━━━━━━


از منوی زیر انتخاب کنید 👇
"""





    await update.message.reply_text(

        text,

        reply_markup=main_menu(

            user.id

        )

        )
    # ==========================================================
# Plans + Orders
# Part 2/10
# ==========================================================



# ==========================================================
# Plans Menu
# ==========================================================


def plans_menu():


    keyboard = [


        [

            InlineKeyboardButton(
                "🥉 اقتصادی | 50GB | 30 روز | 70,000 تومان",
                callback_data="plan_50"
            )

        ],


        [

            InlineKeyboardButton(
                "🥈 ویژه | 100GB | 30 روز | 140,000 تومان",
                callback_data="plan_100"
            )

        ],


        [

            InlineKeyboardButton(
                "🥇 نامحدود | 30 روز | 165,000 تومان",
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

    volume,

    days,

    price

):


    user_id = query.from_user.id





    order_id = create_order(

        user_id,

        volume,

        days,

        price

    )







    await query.edit_message_text(

        f"""
{HEADER}

✅ سفارش شما ثبت شد


🧾 شماره سفارش:

#{order_id}


📦 حجم:

{volume}


⏳ مدت:

{days} روز


💰 مبلغ:

{price:,} تومان


━━━━━━━━━━━━━━


برای پرداخت اقدام کنید 👇
""",

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


async def plan_handler(query):


    if query.data == "plan_50":


        await create_plan_order(

            query,

            "50GB",

            30,

            70000

        )




    elif query.data == "plan_100":


        await create_plan_order(

            query,

            "100GB",

            30,

            140000

        )




    elif query.data == "plan_unlimited":


        await create_plan_order(

            query,

            "Unlimited",

            30,

            165000

            )
        # ==========================================================
# Payment System
# Part 3/10
# ==========================================================



# ==========================================================
# Payment Menu
# ==========================================================


async def payment_menu(query):


    order = last_order(

        query.from_user.id

    )





    if not order:


        await query.edit_message_text(

            f"""
{HEADER}

❌ سفارش فعالی پیدا نشد.


ابتدا یک سرویس انتخاب کنید.
""",

            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "🛒 خرید سرویس",

                            callback_data="buy"

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

        return







    await query.edit_message_text(

        f"""
{HEADER}

💳 پرداخت سفارش


🧾 شماره سفارش:

#{order['id']}


📦 سرویس:

{order['volume']}


⏳ مدت:

{order['days']} روز


💰 مبلغ:

{order['price']:,} تومان


━━━━━━━━━━━━━━


🏦 شماره کارت:

`{CARD_NUMBER}`


━━━━━━━━━━━━━━


بعد از پرداخت:


📸 تصویر رسید را ارسال کنید.


⏳ پس از تایید مدیریت، سرویس شما به صورت خودکار فعال می‌شود.
""",

        parse_mode="Markdown",

        reply_markup=InlineKeyboardMarkup(

            [

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
# Receipt System
# Part 4/10
# ==========================================================



async def receive_receipt(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    try:



        # =========================
        # دریافت فایل رسید
        # =========================


        if update.message.photo:


            file_id = update.message.photo[-1].file_id





        elif update.message.document:


            file_id = update.message.document.file_id





        else:


            await update.message.reply_text(

                f"""
{HEADER}

❌ لطفاً فقط عکس رسید ارسال کنید 📸
"""

            )

            return







        # =========================
        # آخرین سفارش
        # =========================


        order = last_order(

            user.id

        )





        if not order:


            await update.message.reply_text(

                f"""
{HEADER}

❌ سفارش فعالی پیدا نشد.


ابتدا خرید انجام دهید.
"""

            )

            return







        # =========================
        # ذخیره رسید
        # =========================


        save_receipt(

            user.id,

            file_id

        )







        await update.message.reply_text(

            f"""
{HEADER}

✅ رسید دریافت شد.


⏳ منتظر تایید مدیریت باشید.


بعد از تایید، سرویس شما خودکار ساخته می‌شود.
"""

        )







        # =========================
        # ارسال به ادمین
        # =========================


        await context.bot.send_photo(

            chat_id=ADMIN_ID,

            photo=file_id,

            caption=f"""
{HEADER}

💳 رسید پرداخت جدید


👤 کاربر:

{user.first_name}


🆔 آیدی:

{user.id}


🧾 سفارش:

#{order['id']}


📦 حجم:

{order['volume']}


⏳ مدت:

{order['days']} روز


💰 مبلغ:

{order['price']:,} تومان


━━━━━━━━━━━━━━

بررسی پرداخت 👇
""",

            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "✅ تایید",

                            callback_data=f"approve_{order['id']}_{user.id}"

                        )

                    ],

                    [

                        InlineKeyboardButton(

                            "❌ رد",

                            callback_data=f"reject_{order['id']}_{user.id}"

                        )

                    ]

                ]

            )

        )







    except Exception as error:


        print(

            "RECEIPT ERROR:",

            error

        )



        await update.message.reply_text(

            f"""
{HEADER}

❌ خطا در دریافت رسید:


{error}
"""

    )
        # ==========================================================
# Payment Action + Marzban
# Part 5/10
# ==========================================================



async def payment_action(

    query,

    context

):


    data = query.data.split("_")



    action = data[0]

    order_id = int(data[1])

    user_id = int(data[2])







    # فقط ادمین


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return







    # ======================================================
    # Reject Payment
    # ======================================================


    if action == "reject":


        update_order_status(

            order_id,

            "rejected"

        )





        await context.bot.send_message(

            chat_id=user_id,

            text=f"""
{HEADER}

❌ پرداخت شما رد شد.


لطفاً دوباره بررسی کنید یا با پشتیبانی تماس بگیرید 🎧
"""

        )





        await query.edit_message_caption(

            caption=f"""
{HEADER}

❌ پرداخت رد شد.


کاربر مطلع شد.
"""

        )

        return







    # ======================================================
    # Approve Payment
    # ======================================================


    if action == "approve":


        update_order_status(

            order_id,

            "paid"

        )





        await query.edit_message_caption(

            caption=f"""
{HEADER}

⏳ پرداخت تایید شد.


در حال ساخت سرویس...
"""

        )







        try:


            # اتصال به Marzban


            marzban = Marzban()





            service = marzban.create_service(

                volume=50,

                days=30

            )







            if not service:


                await query.edit_message_caption(

                    caption=f"""
{HEADER}

❌ ساخت سرویس ناموفق بود.
"""

                )

                return







            username = service.get(

                "username",

                "unknown"

            )





            subscription_url = (

                service.get(

                    "subscription_url"

                )

                or

                service.get(

                    "subscription"

                )

            )







            save_service(

                user_id,

                username,

                subscription_url,

                service.get(

                    "volume",

                    "50GB"

                ),

                service.get(

                    "days",

                    30

                )

            )







            # ارسال برای مشتری


            await context.bot.send_message(

                chat_id=user_id,

                text=f"""
{HEADER}

🎉 پرداخت تایید شد


✅ سرویس شما فعال شد


👤 نام کاربری:

{username}


📦 حجم:

{service.get('volume')}


⏳ مدت:

{service.get('days')} روز


🔗 لینک اتصال:

{subscription_url}


━━━━━━━━━━━━━━

🙏 ممنون از اعتماد شما
"""

            )







            await query.edit_message_caption(

                caption=f"""
{HEADER}

✅ پرداخت تایید شد


🌐 سرویس ساخته شد


📩 برای مشتری ارسال شد
"""

            )








        except Exception as error:



            print(

                "MARZBAN ERROR:",

                error

            )



            await query.edit_message_caption(

                caption=f"""
{HEADER}

❌ خطا در ساخت سرویس:


{error}
"""

)
            # ==========================================================
# My Service + Discount
# Part 6/10
# ==========================================================



# ==========================================================
# My Service
# ==========================================================


async def my_service(query):


    user_id = query.from_user.id





    service = get_user_service(

        user_id

    )







    if not service:


        await query.edit_message_text(

            f"""
{HEADER}

❌ شما سرویس فعالی ندارید.


برای خرید سرویس اقدام کنید 🛒
""",

            reply_markup=main_menu(

                user_id

            )

        )

        return







    await query.edit_message_text(

        f"""
{HEADER}

🌐 سرویس شما


👤 نام کاربری:

{service['username']}


📦 حجم:

{service['volume']}


⏳ مدت:

{service['days']} روز


🔗 لینک اتصال:

{service['subscription_url']}


━━━━━━━━━━━━━━


🟢 وضعیت:

فعال
""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🔙 منوی اصلی",

                        callback_data="back_home"

                    )

                ]

            ]

        )

    )









# ==========================================================
# Discount Menu
# ==========================================================


async def discount_menu(query):


    await query.edit_message_text(

        f"""
{HEADER}

🎁 کد تخفیف


کد تخفیف خود را ارسال کنید.


نمونه:


ZEUS20


━━━━━━━━━━━━━━

🔥 تخفیف ویژه کاربران
""",

        reply_markup=InlineKeyboardMarkup(

            [

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
# Check Discount Code
# ==========================================================


async def check_discount(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    code = update.message.text.strip().upper()





    discount_codes = {


        "ZEUS20": 20,


        "WELCOME10": 10


    }







    if code in discount_codes:


        percent = discount_codes[code]



        await update.message.reply_text(

            f"""
{HEADER}

✅ کد تخفیف معتبر است


🎁 میزان تخفیف:

{percent}%


در خرید بعدی اعمال خواهد شد.
"""

        )





    else:


        await update.message.reply_text(

            f"""
{HEADER}

❌ کد تخفیف اشتباه است.
"""

        )
        # ==========================================================
# Support System
# Part 7/10
# ==========================================================



# ==========================================================
# Support Menu
# ==========================================================


async def support(query):


    await query.edit_message_text(

        f"""
{HEADER}

🎧 پشتیبانی Zeus Shop VPN


پیام خود را برای مدیریت ارسال کنید.


━━━━━━━━━━━━━━

⚡ پاسخگویی سریع
🔐 پشتیبانی امن
🚀 همراه شما هستیم
""",

        reply_markup=InlineKeyboardMarkup(

            [

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
# Receive User Message
# ==========================================================


async def support_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    message = update.message.text







    # ارسال پیام به ادمین


    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=f"""
{HEADER}

📩 پیام جدید پشتیبانی


👤 کاربر:

{user.first_name}


🆔 آیدی:

{user.id}


━━━━━━━━━━━━━━


💬 پیام:

{message}

━━━━━━━━━━━━━━

برای پاسخ از دکمه زیر استفاده کنید 👇
""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "💬 پاسخ",

                        callback_data=f"reply_{user.id}"

                    )

                ]

            ]

        )

    )







    await update.message.reply_text(

        f"""
{HEADER}

✅ پیام شما ارسال شد.


⏳ منتظر پاسخ پشتیبانی باشید.
"""

    )









# ==========================================================
# Admin Reply
# ==========================================================


async def admin_reply(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if update.effective_user.id != ADMIN_ID:


        return







    user_id = context.user_data.get(

        "reply_user"

    )





    if not user_id:


        return







    await context.bot.send_message(

        chat_id=user_id,

        text=f"""
{HEADER}

🎧 پاسخ پشتیبانی:


{update.message.text}
"""

    )





    context.user_data.clear()





    await update.message.reply_text(

        f"""
{HEADER}

✅ پاسخ ارسال شد.
"""

    )
    # ==========================================================
# Admin Panel System
# Part 8/10
# ==========================================================



# ==========================================================
# Admin Menu
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

                "📦 سفارش‌های در انتظار",

                callback_data="admin_orders"

            )

        ],


        [

            InlineKeyboardButton(

                "➕ افزودن پنل",

                callback_data="add_panel"

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
# Open Admin Panel
# ==========================================================


async def admin_panel(query):


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return







    await query.edit_message_text(

        f"""
{HEADER}

👑 پنل مدیریت


به مدیریت Zeus Shop VPN خوش آمدید.


گزینه مورد نظر را انتخاب کنید 👇
""",

        reply_markup=admin_menu()

    )









# ==========================================================
# Statistics
# ==========================================================


async def admin_stats(query):


    if query.from_user.id != ADMIN_ID:


        return







    stats = get_stats()





    await query.edit_message_text(

        f"""
{HEADER}

📊 آمار ربات


👤 کاربران:

{stats['users']}


🛒 سفارش‌ها:

{stats['orders']}


🌐 سرویس‌ها:

{stats['services']}


💰 درآمد:

{stats['income']:,} تومان


━━━━━━━━━━━━━━
""",

        reply_markup=admin_menu()

    )









# ==========================================================
# Pending Orders
# ==========================================================


async def admin_orders(query):


    if query.from_user.id != ADMIN_ID:


        return







    orders = get_pending_orders()





    if not orders:


        await query.edit_message_text(

            f"""
{HEADER}

📦 سفارش در انتظار وجود ندارد.
""",

            reply_markup=admin_menu()

        )

        return







    text = f"""
{HEADER}

📦 سفارش‌های در انتظار


"""





    for order in orders:


        text += f"""

🧾 سفارش:

#{order['id']}


👤 کاربر:

{order['user_id']}


📦 سرویس:

{order['volume']}


⏳ مدت:

{order['days']} روز


💰 مبلغ:

{order['price']:,} تومان


━━━━━━━━━━━━━━

"""







    await query.edit_message_text(

        text,

        reply_markup=admin_menu()

    )









# ==========================================================
# Add Panel
# ==========================================================


async def add_panel(query):


    if query.from_user.id != ADMIN_ID:


        return







    await query.edit_message_text(

        f"""
{HEADER}

➕ افزودن پنل


مدیریت پنل‌ها


در این بخش می‌توان پنل‌های جدید اضافه کرد.


نمونه:

🌐 Marzban

⚡ 3x-ui

🛡 پنل اختصاصی


━━━━━━━━━━━━━━

نسخه بعدی:
اتصال چند پنل همزمان
""",

        reply_markup=admin_menu()

    )
    # ==========================================================
# Callback Router
# Part 9/10
# ==========================================================



async def button_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data







    # ======================================================
    # Back Home
    # ======================================================


    if data == "back_home":


        await query.edit_message_text(

            f"""
{HEADER}

🏠 منوی اصلی


گزینه مورد نظر را انتخاب کنید 👇
""",

            reply_markup=main_menu(

                query.from_user.id

            )

        )

        return







    # ======================================================
    # Buy
    # ======================================================


    if data == "buy":


        await query.edit_message_text(

            f"""
{HEADER}

🛒 خرید سرویس


پلن مورد نظر را انتخاب کنید 👇
""",

            reply_markup=plans_menu()

        )

        return







    # ======================================================
    # Plans
    # ======================================================


    if data.startswith("plan_"):


        await plan_handler(

            query

        )

        return







    # ======================================================
    # Payment
    # ======================================================


    if data == "payment":


        await payment_menu(

            query

        )

        return







    # ======================================================
    # My Service
    # ======================================================


    if data == "my_service":


        await my_service(

            query

        )

        return







    # ======================================================
    # Discount
    # ======================================================


    if data == "discount":


        await discount_menu(

            query

        )

        return







    # ======================================================
    # Support
    # ======================================================


    if data == "support":


        await support(

            query

        )

        return







    # ======================================================
    # Help
    # ======================================================


    if data == "help":


        await help_menu(

            query

        )

        return







    # ======================================================
    # Admin
    # ======================================================


    if data == "admin":


        await admin_panel(

            query

        )

        return







    if data == "admin_stats":


        await admin_stats(

            query

        )

        return







    if data == "admin_orders":


        await admin_orders(

            query

        )

        return







    if data == "add_panel":


        await add_panel(

            query

        )

        return







    # ======================================================
    # Approve / Reject Payment
    # ======================================================


    if (

        data.startswith("approve_")

        or

        data.startswith("reject_")

    ):


        await payment_action(

            query,

            context

        )

        return







    # ======================================================
    # Admin Reply
    # ======================================================


    if data.startswith("reply_"):


        user_id = int(

            data.split("_")[1]

        )


        context.user_data["reply_user"] = user_id



        await query.message.reply_text(

            """
💬 پاسخ خود را ارسال کنید:
"""

        )

        return
        # ==========================================================
# Register Handlers
# Part 10/10
# ==========================================================



def register_handlers(application):


    # ======================================================
    # Start
    # ======================================================


    application.add_handler(

        CommandHandler(

            "start",

            start

        )

    )







    # ======================================================
    # Receipt Upload
    # مهم:
    # قبل از Text Handler
    # ======================================================


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_receipt

        )

    )





    application.add_handler(

        MessageHandler(

            filters.Document.ALL,

            receive_receipt

        )

    )







    # ======================================================
    # Admin Reply
    # ======================================================


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            admin_reply

        )

    )







    # ======================================================
    # Buttons
    # ======================================================


    application.add_handler(

        CallbackQueryHandler(

            button_handler

        )

    )







    # ======================================================
    # Support Messages
    # ======================================================


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            support_message

        )

    )







    print(

        "✅ Zeus Shop VPN CLEAN PRO Loaded"

        )
