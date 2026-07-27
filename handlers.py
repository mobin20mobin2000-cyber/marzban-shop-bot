# ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 1/8
# ==========================================================


# ==========================
# Telegram Imports
# ==========================

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





# ==========================
# Config
# ==========================

from config import (
    ADMIN_ID,
    CARD_NUMBER
)





# ==========================
# Database
# ==========================

from database import (

    add_user,

    create_order,

    last_order,

    get_order,

    save_receipt,

    save_service,

    get_user_service,

    get_stats,

    get_pending_orders,

    update_order_status,

    get_all_users

)





# ==========================
# Marzban
# ==========================

from marzban import Marzban





# ==========================
# Broadcast
# ==========================

from broadcast import (

    broadcast_message

)







# ==========================================================
# Style
# ==========================================================


HEADER = """

━━━━━━━━━━━━━━━━━━

👑 Zeus Shop VPN

━━━━━━━━━━━━━━━━━━

"""









# ==========================================================
# User Main Menu
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
                    "👑 پنل مدیریت",
                    callback_data="admin"
                )

            ]

        )





    return InlineKeyboardMarkup(
        keyboard
    )









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
                "📦 سفارش‌ها",
                callback_data="admin_orders"
            )

        ],


        [

            InlineKeyboardButton(
                "📢 پیام همگانی",
                callback_data="broadcast"
            )

        ],


        [

            InlineKeyboardButton(
                "📣 پیام فروش",
                callback_data="sales_message"
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
# /start Command
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


━━━━━━━━━━━━━━━━━━


⚡ فعالسازی سریع سرویس

🌍 سرورهای پرسرعت

🔐 اتصال امن

🎧 پشتیبانی فعال


━━━━━━━━━━━━━━━━━━


از منوی زیر انتخاب کنید 👇

"""





    await update.message.reply_text(

        text,

        reply_markup=main_menu(

            user.id

        )

    )
    # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 2/8
# ==========================================================


# ==========================================================
# Plans Menu
# ==========================================================


def plans_menu():


    keyboard = [


        [

            InlineKeyboardButton(
                "🥉 اقتصادی | 50GB | 30 روز",
                callback_data="plan_50"
            )

        ],


        [

            InlineKeyboardButton(
                "🥈 ویژه | 100GB | 30 روز",
                callback_data="plan_100"
            )

        ],


        [

            InlineKeyboardButton(
                "🥇 نامحدود | 30 روز",
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
# Buy Menu
# ==========================================================


async def buy_menu(query):


    await query.edit_message_text(

        f"""

{HEADER}

🛒 خرید سرویس


پلن مورد نظر خود را انتخاب کنید 👇

""",

        reply_markup=plans_menu()

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


━━━━━━━━━━━━━━━━━━


اکنون پرداخت را انجام دهید 👇

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


    data = query.data





    if data == "plan_50":


        await create_plan_order(

            query,

            "50GB",

            30,

            70000

        )





    elif data == "plan_100":


        await create_plan_order(

            query,

            "100GB",

            30,

            140000

        )





    elif data == "plan_unlimited":


        await create_plan_order(

            query,

            "Unlimited",

            30,

            165000

        )
        # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 3/8
# ==========================================================


# ==========================================================
# Payment Menu
# ==========================================================


async def payment_menu(query):


    user_id = query.from_user.id





    order = last_order(

        user_id

    )





    if not order:


        await query.edit_message_text(

            f"""

{HEADER}

❌ سفارش فعالی پیدا نشد.


ابتدا یک سرویس خریداری کنید 🛒

""",

            reply_markup=main_menu(

                user_id

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


━━━━━━━━━━━━━━━━━━


🏦 شماره کارت:


`{CARD_NUMBER}`


━━━━━━━━━━━━━━━━━━


بعد از پرداخت، عکس رسید را ارسال کنید 📸

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
# Receive Payment Receipt
# ==========================================================


async def receive_receipt(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    try:


        file_id = None





        # Photo Receipt

        if update.message.photo:


            file_id = update.message.photo[-1].file_id





        # Document Receipt

        elif update.message.document:


            file_id = update.message.document.file_id





        if not file_id:


            await update.message.reply_text(

                f"""

{HEADER}

❌ لطفاً عکس رسید ارسال کنید 📸

"""

            )

            return







        order = last_order(

            user.id

        )





        if not order:


            await update.message.reply_text(

                f"""

{HEADER}

❌ سفارش فعالی ندارید.


ابتدا خرید انجام دهید.

"""

            )

            return







        # Save Receipt

        save_receipt(

            user.id,

            order["id"],

            file_id

        )







        await update.message.reply_text(

            f"""

{HEADER}

✅ رسید شما دریافت شد.


⏳ منتظر تایید مدیریت باشید.


بعد از تایید، سرویس ساخته می‌شود 🚀

"""

        )







        # Send To Admin


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


📦 سرویس:

{order['volume']}


⏳ مدت:

{order['days']} روز


💰 مبلغ:

{order['price']:,} تومان


━━━━━━━━━━━━━━━━━━


بررسی پرداخت 👇

""",

            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "✅ تایید پرداخت",

                            callback_data=f"approve_{order['id']}_{user.id}"

                        )

                    ],


                    [

                        InlineKeyboardButton(

                            "❌ رد پرداخت",

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

❌ خطا:


{error}

"""

    )
        # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 4/8
# ==========================================================


# ==========================================================
# Payment Approve / Reject
# ==========================================================


async def payment_action(

    query,

    context

):


    data = query.data.split("_")


    action = data[0]

    order_id = int(data[1])

    user_id = int(data[2])





    # Only Admin


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return







    order = get_order(

        order_id

    )







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


اگر مشکلی وجود دارد با پشتیبانی تماس بگیرید 🎧

"""

        )





        await query.edit_message_caption(

            caption=f"""

{HEADER}

❌ پرداخت رد شد.


کاربر اطلاع داده شد.

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





        try:


            await query.edit_message_caption(

                caption=f"""

{HEADER}

⏳ در حال ساخت سرویس...


لطفاً صبر کنید 🚀

"""

            )







            # Order Info


            volume = order["volume"]

            days = order["days"]







            # Convert Volume


            if volume == "50GB":


                volume_value = 50



            elif volume == "100GB":


                volume_value = 100



            else:


                volume_value = 0







            # Create Marzban Service


            marzban = Marzban()





            service = marzban.create_service(

                volume=volume_value,

                days=days

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





            subscription = (

                service.get(

                    "subscription_url"

                )

                or

                service.get(

                    "subscription"

                )

            )







            if not subscription:


                await query.edit_message_caption(

                    caption=f"""

{HEADER}

❌ لینک اتصال دریافت نشد.

"""

                )

                return







            # Save Service


            save_service(

                user_id,

                username,

                subscription,

                volume,

                days

            )







            # Send User


            await context.bot.send_message(

                chat_id=user_id,

                text=f"""

{HEADER}

🎉 پرداخت تایید شد


✅ سرویس شما فعال شد


👤 نام کاربری:

{username}


📦 حجم:

{volume}


⏳ مدت:

{days} روز


🔗 لینک اتصال:

{subscription}


━━━━━━━━━━━━━━━━━━


🙏 ممنون از اعتماد شما

"""

            )







            # Update Admin Message


            await query.edit_message_caption(

                caption=f"""

{HEADER}

✅ پرداخت تایید شد


🌐 سرویس ساخته شد


📩 اطلاعات برای مشتری ارسال شد.

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
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 5/8
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


━━━━━━━━━━━━━━━━━━


🟢 وضعیت:

فعال ✅

""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🔄 تمدید سرویس",

                        callback_data="renew"

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
# Renew Service
# ==========================================================


async def renew_service(query):


    await query.edit_message_text(

        f"""

{HEADER}

🔄 تمدید سرویس


پلن تمدید را انتخاب کنید 👇

""",

        reply_markup=plans_menu()

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


━━━━━━━━━━━━━━━━━━


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
# Check Discount
# ==========================================================


async def check_discount(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    code = update.message.text.strip().upper()







    discount_codes = {


        "ZEUS20": 20,


        "WELCOME10": 10,


        "VIP30": 30


    }









    if code in discount_codes:


        percent = discount_codes[code]





        await update.message.reply_text(

            f"""

{HEADER}

✅ کد تخفیف معتبر است


🎁 مقدار تخفیف:

{percent}%


در خرید شما اعمال می‌شود 🚀

"""

        )







    else:


        await update.message.reply_text(

            f"""

{HEADER}

❌ کد تخفیف اشتباه است.


دوباره تلاش کنید.

"""

        )









# ==========================================================
# Customer Notification
# ==========================================================


async def notify_customer(

    bot,

    user_id,

    title,

    message

):


    try:


        await bot.send_message(

            chat_id=user_id,

            text=f"""

{HEADER}

{title}


{message}


━━━━━━━━━━━━━━━━━━


❤️ Zeus Shop VPN

"""

        )



    except Exception as error:


        print(

            "NOTIFY ERROR:",

            error

        )









# ==========================================================
# Service Notification
# ==========================================================


async def service_notification(

    bot,

    user_id

):


    await notify_customer(

        bot,

        user_id,

        "🌐 وضعیت سرویس",

        """
سرویس شما فعال است.


در صورت نیاز به پشتیبانی با ما تماس بگیرید.
"""

    )
    # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 6/8
# ==========================================================


# ==========================================================
# Support Menu
# ==========================================================


async def support(query):


    await query.edit_message_text(

        f"""

{HEADER}

🎧 پشتیبانی Zeus Shop VPN


پیام خود را ارسال کنید.


━━━━━━━━━━━━━━━━━━


⚡ پاسخگویی سریع

🔐 پشتیبانی امن

🚀 همراه شما هستیم


━━━━━━━━━━━━━━━━━━


پیام خود را بنویسید 👇

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
# Receive User Support Message
# ==========================================================


async def support_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    message = update.message.text







    # جلوگیری از تداخل با حالت‌های دیگر


    if context.user_data.get(

        "reply_mode"

    ):


        return







    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=f"""

{HEADER}

📩 پیام پشتیبانی جدید


👤 نام:

{user.first_name}


🆔 آیدی:

{user.id}


━━━━━━━━━━━━━━━━━━


💬 پیام:


{message}


━━━━━━━━━━━━━━━━━━


برای پاسخ روی دکمه زیر بزنید 👇

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


⏳ منتظر پاسخ مدیریت باشید.

"""

    )









# ==========================================================
# Start Admin Reply
# ==========================================================


async def start_admin_reply(

    query,

    context

):


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return







    user_id = int(

        query.data.split("_")[1]

    )







    context.user_data["reply_user"] = user_id


    context.user_data["reply_mode"] = True







    await query.message.reply_text(

        """

💬 متن پاسخ خود را ارسال کنید:

"""

    )









# ==========================================================
# Send Admin Reply
# ==========================================================


async def admin_reply(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if update.effective_user.id != ADMIN_ID:


        return







    if not context.user_data.get(

        "reply_mode"

    ):


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


━━━━━━━━━━━━━━━━━━


👑 Zeus Shop VPN

"""

    )







    context.user_data.clear()







    await update.message.reply_text(

        f"""

{HEADER}

✅ پاسخ برای مشتری ارسال شد.

"""

    )









# ==========================================================
# Cancel Operation
# ==========================================================


async def cancel_operation(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    context.user_data.clear()





    await update.message.reply_text(

        f"""

{HEADER}

❌ عملیات لغو شد.

"""

    )
    # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 7/8
# ==========================================================


# ==========================================================
# Admin Panel
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

👑 پنل مدیریت Zeus Shop VPN


به بخش مدیریت خوش آمدید.


گزینه مورد نظر را انتخاب کنید 👇

""",

        reply_markup=admin_menu()

    )









# ==========================================================
# Admin Statistics
# ==========================================================


async def admin_stats(query):


    if query.from_user.id != ADMIN_ID:


        return







    stats = get_stats()







    await query.edit_message_text(

        f"""

{HEADER}

📊 آمار ربات


👥 کاربران:

{stats['users']}


🛒 سفارش‌ها:

{stats['orders']}


🌐 سرویس‌ها:

{stats['services']}


💰 درآمد:

{stats['income']:,} تومان


━━━━━━━━━━━━━━━━━━

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


━━━━━━━━━━━━━━━━━━

"""







    await query.edit_message_text(

        text,

        reply_markup=admin_menu()

    )









# ==========================================================
# Add Panel Menu
# ==========================================================


async def add_panel(query):


    if query.from_user.id != ADMIN_ID:


        return







    await query.edit_message_text(

        f"""

{HEADER}

➕ افزودن پنل


این بخش برای مدیریت چند پنل ساخته شده است.


پنل‌های قابل پشتیبانی:


🌐 Marzban

⚡ 3x-ui

🛡 پنل اختصاصی


━━━━━━━━━━━━━━━━━━


در نسخه‌های بعدی اتصال چند پنل فعال می‌شود.

""",

        reply_markup=admin_menu()

    )









# ==========================================================
# Sales Message Menu
# ==========================================================


async def sales_message_menu(

    query,

    context

):


    if query.from_user.id != ADMIN_ID:


        return







    context.user_data["sales_mode"] = True







    await query.edit_message_text(

        f"""

{HEADER}

📣 پیام فروش


متن تبلیغاتی خود را ارسال کنید.


مثال:


🔥 تخفیف ویژه امروز


💎 سرویس‌های جدید فعال شد

"""

    )









# ==========================================================
# Send Sales Message
# ==========================================================


async def send_sales_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if update.effective_user.id != ADMIN_ID:


        return







    if not context.user_data.get(

        "sales_mode"

    ):


        return







    message = update.message.text





    users = get_all_users()





    success = 0

    failed = 0







    for user in users:


        try:


            await context.bot.send_message(

                chat_id=user["user_id"],

                text=f"""

{HEADER}

📣 اطلاعیه ویژه


{message}


━━━━━━━━━━━━━━━━━━


👑 Zeus Shop VPN

"""

            )


            success += 1





        except Exception:


            failed += 1







    context.user_data.clear()







    await update.message.reply_text(

        f"""

{HEADER}

✅ پیام فروش ارسال شد


📨 موفق:

{success}


❌ ناموفق:

{failed}

"""

    )
    # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 8/8
# ==========================================================


# ==========================================================
# Broadcast System
# ==========================================================


async def broadcast_menu(

    query,

    context

):


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return







    context.user_data["broadcast_mode"] = True







    await query.edit_message_text(

        f"""

{HEADER}

📢 ارسال پیام همگانی


متن پیام خود را ارسال کنید ✍️


این پیام برای تمام کاربران ارسال می‌شود.


برای لغو:

لغو

"""

    )









# ==========================================================
# Receive Broadcast Message
# ==========================================================


async def receive_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if update.effective_user.id != ADMIN_ID:


        return







    if not context.user_data.get(

        "broadcast_mode"

    ):


        return







    message = update.message.text







    if message.lower() == "لغو":


        context.user_data.clear()



        await update.message.reply_text(

            f"""

{HEADER}

❌ ارسال پیام لغو شد.

"""

        )


        return







    await update.message.reply_text(

        f"""

{HEADER}

⏳ در حال ارسال پیام...


لطفاً صبر کنید.

"""

    )







    try:


        result = await broadcast_message(

            context.bot,

            message

        )







        await update.message.reply_text(

            f"""

{HEADER}

✅ ارسال همگانی انجام شد


👥 کل کاربران:

{result['total']}


✅ موفق:

{result['success']}


❌ ناموفق:

{result['failed']}


━━━━━━━━━━━━━━━━━━

"""

        )







    except Exception as error:


        await update.message.reply_text(

            f"""

{HEADER}

❌ خطا:


{error}

"""

        )







    context.user_data.clear()











# ==========================================================
# Callback Router
# ==========================================================


async def button_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data







    if data == "back_home":


        await query.edit_message_text(

            f"""

{HEADER}

🏠 منوی اصلی


انتخاب کنید 👇

""",

            reply_markup=main_menu(

                query.from_user.id

            )

        )


        return







    if data == "buy":


        await buy_menu(

            query

        )

        return







    if data.startswith("plan_"):


        await plan_handler(

            query

        )

        return







    if data == "payment":


        await payment_menu(

            query

        )

        return







    if data == "my_service":


        await my_service(

            query

        )

        return







    if data == "renew":


        await renew_service(

            query

        )

        return







    if data == "discount":


        await discount_menu(

            query

        )

        return







    if data == "support":


        await support(

            query

        )

        return







    if data == "help":


        await help_menu(

            query

        )

        return







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







    if data == "broadcast":


        await broadcast_menu(

            query,

            context

        )

        return







    if data == "sales_message":


        await sales_message_menu(

            query,

            context

        )

        return







    if data == "add_panel":


        await add_panel(

            query

        )

        return







    if data.startswith("reply_"):


        await start_admin_reply(

            query,

            context

        )

        return







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







# ==========================================================
# Help Menu
# ==========================================================


async def help_menu(query):


    await query.edit_message_text(

        f"""

{HEADER}

ℹ️ راهنمای Zeus Shop VPN


🛒 خرید سرویس:

انتخاب پلن و پرداخت


💳 پرداخت:

ارسال رسید بانکی


👤 سرویس من:

مشاهده لینک اتصال


🎧 پشتیبانی:

ارتباط با مدیریت


🎁 تخفیف:

استفاده از کدهای ویژه


━━━━━━━━━━━━━━━━━━


❤️ ممنون از اعتماد شما

""",

        reply_markup=main_menu(

            query.from_user.id

        )

    )









# ==========================================================
# Register Handlers
# ==========================================================


def register_handlers(application):


    # Start Command


    application.add_handler(

        CommandHandler(

            "start",

            start

        )

    )







    # Callback Buttons


    application.add_handler(

        CallbackQueryHandler(

            button_handler

        )

    )







    # Payment Receipt Photo


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_receipt

        )

    )







    # Payment Receipt File


    application.add_handler(

        MessageHandler(

            filters.Document.ALL,

            receive_receipt

        )

    )







    # Text Messages


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            receive_broadcast

        )

    )







    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            admin_reply

        )

    )







    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            support_message

        )

    )







    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            check_discount

        )

    )







    print(

        "✅ Zeus Shop VPN PRO FINAL Loaded"

            )
