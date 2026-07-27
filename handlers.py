# ==========================================================
# Zeus Shop VPN PRO CLEAN
# handlers.py
# Part 1/10
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
# Main User Menu
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







    # Admin Button


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
# Start System
# Part 2/10
# ==========================================================



# ==========================================================
# /start Command
# ==========================================================


async def start(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    # ثبت کاربر در دیتابیس

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

🔐 اتصال امن و پایدار

🎧 پشتیبانی آنلاین


━━━━━━━━━━━━━━━━━━


از منوی زیر سرویس مورد نظر خود را انتخاب کنید 👇

"""







    await update.message.reply_text(

        text,

        reply_markup=main_menu(

            user.id

        )

    )









# ==========================================================
# Welcome Notification
# ==========================================================


async def welcome_message(

    bot,

    user_id

):


    try:


        await bot.send_message(

            chat_id=user_id,

            text=f"""

{HEADER}

🎉 خوش آمدید به خانواده Zeus Shop VPN


برای شروع، از منوی ربات سرویس خود را انتخاب کنید.


🚀 اینترنت سریع‌تر

🔐 اتصال امن

💎 پشتیبانی حرفه‌ای

"""

        )



    except Exception as error:


        print(

            "WELCOME ERROR:",

            error

    )
        # ==========================================================
# Plans & Orders System
# Part 3/10
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
# Payment & Receipt System
# Part 4/10
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


ابتدا یک سرویس خریداری کنید 🛒

""",

            reply_markup=main_menu(

                query.from_user.id

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
# Receive Receipt
# ==========================================================


async def receive_receipt(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    try:



        # دریافت فایل رسید


        if update.message.photo:


            file_id = update.message.photo[-1].file_id





        elif update.message.document:


            file_id = update.message.document.file_id





        else:


            await update.message.reply_text(

                f"""

{HEADER}

❌ لطفاً عکس رسید ارسال کنید 📸

"""

            )

            return







        # آخرین سفارش


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







        # ذخیره رسید


        save_receipt(

            user.id,

            file_id

        )







        # پیام به مشتری


        await update.message.reply_text(

            f"""

{HEADER}

✅ رسید شما دریافت شد.


⏳ منتظر تایید مدیریت باشید.


بعد از تایید، سرویس شما ساخته می‌شود 🚀

"""

        )







        # ارسال برای ادمین


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

بررسی کنید 👇

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
# Payment Action
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







    # گرفتن اطلاعات سفارش


    order = None


    try:


        order = get_order(

            order_id

        )


    except Exception as error:


        print(

            "ORDER ERROR:",

            error

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

❌ پرداخت شما تایید نشد.


اگر اشتباهی رخ داده است با پشتیبانی تماس بگیرید 🎧

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


لطفاً صبر کنید.

"""

            )







            # اطلاعات سفارش


            volume = "50GB"

            days = 30





            if order:


                volume = order["volume"]

                days = order["days"]







            # تبدیل حجم


            if volume == "50GB":


                volume_value = 50



            elif volume == "100GB":


                volume_value = 100



            else:


                volume_value = 0







            # ساخت سرویس


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







            # ذخیره سرویس


            save_service(

                user_id,

                username,

                subscription,

                volume,

                days

            )







            # ارسال به مشتری


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







            # پیام ادمین


            await query.edit_message_caption(

                caption=f"""

{HEADER}

✅ پرداخت تایید شد


🌐 سرویس ساخته شد


📩 برای مشتری ارسال شد.

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
# My Service & Discount
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


برای خرید سرویس از منوی خرید استفاده کنید 🛒

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

فعال

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


برای تمدید سرویس، یکی از پلن‌ها را انتخاب کنید 👇

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


🔥 تخفیف ویژه مشتریان

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


        "WELCOME10": 10,


        "VIP30": 30



    }









    if code in discount_codes:



        percent = discount_codes[code]





        await update.message.reply_text(

            f"""

{HEADER}

✅ کد تخفیف تایید شد


🎁 مقدار تخفیف:

{percent}%


در خرید بعدی اعمال می‌شود 🚀

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


async def send_customer_notification(

    bot,

    user_id,

    message

):


    try:



        await bot.send_message(

            chat_id=user_id,

            text=f"""

{HEADER}

📢 اطلاعیه Zeus Shop VPN


{message}

━━━━━━━━━━━━━━━━━━

❤️ با تشکر از همراهی شما

"""

        )





    except Exception as error:


        print(

            "NOTIFICATION ERROR:",

            error

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
# User Send Support Message
# ==========================================================


async def support_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user





    message = update.message.text







    # جلوگیری از تداخل


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


⏳ منتظر پاسخ پشتیبانی باشید.

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

💬 متن پاسخ را ارسال کنید:

"""

    )









# ==========================================================
# Send Admin Reply To User
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

Zeus Shop VPN

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
# Cancel Reply
# ==========================================================


async def cancel_reply(

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
# Admin System
# Part 8/10
# ==========================================================



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

👑 پنل مدیریت Zeus Shop VPN


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


📦 حجم:

{order['volume']}


⏳ مدت:

{order['days']} روز


💰 مبلغ:

{order['price']:,}


━━━━━━━━━━━━━━━━━━

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


این بخش برای اتصال پنل‌های بیشتر است.


پشتیبانی آینده:


🌐 Marzban

⚡ 3x-ui

🛡 پنل‌های دیگر


━━━━━━━━━━━━━━━━━━

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


متن پیام تبلیغاتی خود را ارسال کنید:


مثال:


🔥 تخفیف ویژه امروز


50٪ تخفیف سرویس‌ها

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


Zeus Shop VPN

"""

            )


            success += 1



        except:


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
# Broadcast System
# Part 9/10
# ==========================================================



# ==========================================================
# Broadcast Menu
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
# Receive Broadcast
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







    # لغو


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

❌ خطا در ارسال:


{error}

"""

        )







    context.user_data.clear()









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

            "CUSTOMER NOTIFY ERROR:",

            error

        )









# ==========================================================
# Send Service Notification
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


در صورت نیاز به پشتیبانی با ما در تماس باشید.
"""

    )









# ==========================================================
# Sales Notification
# ==========================================================


async def sales_notification(

    bot,

    user_id

):


    await notify_customer(

        bot,

        user_id,

        "🔥 پیشنهاد ویژه",

        """
تخفیف‌های جدید Zeus Shop VPN فعال شد.


برای خرید سرویس وارد ربات شوید 🚀
"""

    )
    # ==========================================================
# Callback Router
# Part 10/10
# ==========================================================



async def button_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data







    # ======================================================
    # Home
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
    # Renew
    # ======================================================


    if data == "renew":


        await renew_service(

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
    # Broadcast
    # ======================================================


    if data == "broadcast":


        await broadcast_menu(

            query,

            context

        )


        return







    # ======================================================
    # Sales Message
    # ======================================================


    if data == "sales_message":


        await sales_message_menu(

            query,

            context

        )


        return







    # ======================================================
    # Support Reply
    # ======================================================


    if data.startswith("reply_"):


        await start_admin_reply(

            query,

            context

        )


        return







    # ======================================================
    # Payment Approve Reject
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

ارتباط مستقیم


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


    # Start


    application.add_handler(

        CommandHandler(

            "start",

            start

        )

    )







    # Buttons


    application.add_handler(

        CallbackQueryHandler(

            button_handler

        )

    )







    # Receipt Photo


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_receipt

        )

    )







    # Receipt Document


    application.add_handler(

        MessageHandler(

            filters.Document.ALL,

            receive_receipt

        )

    )







    # Broadcast


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            receive_broadcast

        )

    )







    # Admin Reply


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            admin_reply

        )

    )







    # Support


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            support_message

        )

    )







    # Discount


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            check_discount

        )

    )







    print(

        "✅ Zeus Shop VPN PRO CLEAN Loaded"

        )
