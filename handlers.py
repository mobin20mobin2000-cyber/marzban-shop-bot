# ==========================================================
# Zeus Shop VPN PRO
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
                "🎧 پشتیبانی",
                callback_data="support"
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
👑 Zeus Shop VPN

سلام {user.first_name} عزیز 🌹

به ربات رسمی خرید VPN خوش آمدید 🚀

━━━━━━━━━━━━━━

⚡ فعالسازی سریع
🌍 سرور پرسرعت
🔐 اتصال امن
🎧 پشتیبانی آنلاین

━━━━━━━━━━━━━━

از منوی زیر انتخاب کنید 👇
"""



    await update.message.reply_text(

        text,

        reply_markup=main_menu(user.id)

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
✅ سفارش ثبت شد

━━━━━━━━━━━━━━

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
# Payment
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

            """
❌ سفارش فعالی پیدا نشد.

ابتدا یک سرویس خریداری کنید.
"""

        )

        return







    await query.edit_message_text(

        f"""
💳 پرداخت سفارش

━━━━━━━━━━━━━━

🧾 شماره سفارش:

#{order['id']}


📦 حجم:

{order['volume']}


⏳ مدت:

{order['days']} روز


💰 مبلغ:

{order['price']:,} تومان


🏦 شماره کارت:

{CARD_NUMBER}

━━━━━━━━━━━━━━

بعد از پرداخت عکس رسید را ارسال کنید.

⚠️ فقط عکس رسید ارسال کنید.
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
# Receipt Handler
# Part 4/10
# ==========================================================



async def receive_receipt(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    print(
        "🔥 RECEIPT FUNCTION CALLED"
    )



    user = update.effective_user





    try:



        # دریافت عکس

        if update.message.photo:


            file_id = update.message.photo[-1].file_id





        elif update.message.document:


            file_id = update.message.document.file_id





        else:


            await update.message.reply_text(

                "❌ لطفاً عکس رسید ارسال کنید."

            )

            return







        order = last_order(

            user.id

        )





        if not order:


            await update.message.reply_text(

                """
❌ سفارشی برای پرداخت پیدا نشد.

ابتدا خرید انجام دهید.
"""

            )

            return







        # ذخیره رسید

        save_receipt(

            user.id,

            file_id

        )







        await update.message.reply_text(

            """
✅ رسید شما دریافت شد.

⏳ منتظر تایید مدیریت باشید.
"""

        )







        # ارسال برای ادمین


        await context.bot.send_photo(

            chat_id=ADMIN_ID,

            photo=file_id,

            caption=f"""
💳 رسید پرداخت جدید

━━━━━━━━━━━━━━

👤 کاربر:

{user.first_name}


🆔 آیدی:

{user.id}


🧾 سفارش:

#{order['id']}


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



        print(

            "✅ RECEIPT SENT TO ADMIN"

        )







    except Exception as error:



        print(

            "❌ RECEIPT ERROR:",

            error

        )



        await update.message.reply_text(

            f"""
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

            text="""
❌ پرداخت شما رد شد.

لطفاً با پشتیبانی تماس بگیرید.
"""

        )





        await query.edit_message_caption(

            caption="""
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





        try:



            marzban = Marzban()





            service = marzban.create_service(

                volume=50,

                days=30

            )





            if not service:


                await query.edit_message_caption(

                    caption="""
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







            if not subscription_url:


                await query.edit_message_caption(

                    caption="""
❌ لینک اشتراک پیدا نشد.
"""

                )

                return







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








            await context.bot.send_message(

                chat_id=user_id,

                text=f"""
🎉 پرداخت شما تایید شد

━━━━━━━━━━━━━━

👤 نام کاربری:

{username}


📦 حجم:

{service.get('volume')}


⏳ مدت:

{service.get('days')} روز


🔗 لینک اتصال:

{subscription_url}

━━━━━━━━━━━━━━

❤️ ممنون از اعتماد شما
"""

            )








            await query.edit_message_caption(

                caption="""
✅ پرداخت تایید شد

✅ سرویس ساخته شد

✅ برای کاربر ارسال شد
"""

            )







        except Exception as error:



            print(

                "❌ MARZBAN ERROR:",

                error

            )



            await query.edit_message_caption(

                caption=f"""
❌ خطا در ساخت سرویس:

{error}
"""

            )
            # ==========================================================
# My Service
# Part 6/10
# ==========================================================



async def my_service(query):


    user_id = query.from_user.id





    service = get_user_service(

        user_id

    )







    if not service:



        await query.edit_message_text(

            """
❌ شما سرویس فعالی ندارید.

برای خرید سرویس اقدام کنید.
""",

            reply_markup=main_menu(user_id)

        )

        return







    await query.edit_message_text(

        f"""
🌐 سرویس شما

━━━━━━━━━━━━━━

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

        reply_markup=main_menu(user_id)

        )
    # ==========================================================
# Admin Panel
# Part 7/10
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

        """
👑 پنل مدیریت Zeus Shop VPN

━━━━━━━━━━━━━━

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
📊 آمار ربات

━━━━━━━━━━━━━━

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
# Admin Orders + Support
# Part 8/10
# ==========================================================



# ==========================================================
# Pending Orders
# ==========================================================


async def admin_orders(query):


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return







    orders = get_pending_orders()





    if not orders:


        await query.edit_message_text(

            """
📦 سفارش در انتظار وجود ندارد.
""",

            reply_markup=admin_menu()

        )

        return







    text = """
📦 سفارش‌های در انتظار

━━━━━━━━━━━━━━
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
{order['price']:,} تومان

━━━━━━━━━━━━━━
"""







    await query.edit_message_text(

        text,

        reply_markup=admin_menu()

    )









# ==========================================================
# Support
# ==========================================================


async def support(query):


    await query.edit_message_text(

        """
🎧 پشتیبانی Zeus Shop VPN

━━━━━━━━━━━━━━

برای ارتباط با مدیریت پیام خود را ارسال کنید.

⚡ پاسخگویی سریع
🔐 امنیت بالا
🚀 سرویس پایدار
"""

    )
    # ==========================================================
# Button Handler
# Part 9/10
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

            reply_markup=main_menu(

                query.from_user.id

            )

        )

        return







    # =========================
    # Buy Menu
    # =========================


    if data == "buy":


        await query.edit_message_text(

            "🛒 سرویس مورد نظر را انتخاب کنید 👇",

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
    # Payment
    # =========================


    if data == "payment":


        await payment_menu(

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
    # Support
    # =========================


    if data == "support":


        await support(

            query

        )

        return







    # =========================
    # Admin
    # =========================


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







    # =========================
    # Approve / Reject Receipt
    # =========================


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
# Register Handlers
# Part 10/10
# ==========================================================



def register_handlers(application):


    # =========================
    # Start
    # =========================


    application.add_handler(

        CommandHandler(

            "start",

            start

        )

    )







    # =========================
    # Receipt
    # مهم:
    # قبل از Text Handler
    # =========================


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







    # =========================
    # Buttons
    # =========================


    application.add_handler(

        CallbackQueryHandler(

            button_handler

        )

    )







    # =========================
    # Text Messages
    # =========================


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            support

        )

    )







    print(

        "✅ Zeus Shop VPN PRO Loaded"

    )
    
