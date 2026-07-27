# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 1/7
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
    get_user_service,
    save_service,
    get_stats,
    update_order_status
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



    # فقط ادمین اصلی ببیند

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


به ربات رسمی فروش VPN خوش آمدید.


━━━━━━━━━━━━


🚀 اتصال پرسرعت

🔐 امنیت بالا

⚡ فعالسازی سریع

🌍 مناسب تمام دستگاه‌ها


━━━━━━━━━━━━


از منوی زیر انتخاب کنید 👇

"""



    await update.message.reply_text(

        text,

        reply_markup=main_menu(user.id)

    )
    # ==========================================================
# Plans + Orders
# Part 2/7
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
                "🎟 وارد کردن کد تخفیف",
                callback_data="discount"
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

✅ سفارش شما ثبت شد


━━━━━━━━━━━━


🧾 شماره سفارش:

#{order_id}


📦 حجم:

{volume}


⏳ مدت:

{days} روز


💰 مبلغ:

{price:,} تومان


━━━━━━━━━━━━


برای پرداخت اقدام کنید.

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

                        "🔙 برگشت",

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
# Payment + Receipt
# Part 3/7
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


ابتدا سرویس خریداری کنید.

"""

        )

        return





    await query.edit_message_text(

        f"""

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

    )









# ==========================================================
# Receive Receipt
# ==========================================================


async def receive_receipt(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user



    order = last_order(

        user.id

    )



    if not order:


        await update.message.reply_text(

            "❌ سفارش فعالی ندارید."

        )

        return






    if not update.message.photo:


        await update.message.reply_text(

            "❌ فقط عکس رسید ارسال کنید."

        )

        return





    photo = update.message.photo[-1]



    # ذخیره رسید

    save_receipt(

        user.id,

        photo.file_id

    )





    await update.message.reply_text(

        """

✅ رسید دریافت شد.


⏳ منتظر تایید مدیریت باشید.

"""

    )







    # ارسال برای ادمین


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


🧾 سفارش:

#{order['id']}


💰 مبلغ:

{order['price']:,} تومان


━━━━━━━━━━━━


بررسی پرداخت

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
    # ==========================================================
# Payment Approval + Marzban
# Part 4/7
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
    # Reject
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


در صورت مشکل با پشتیبانی تماس بگیرید.

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
    # Approve
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

❌ ساخت سرویس Marzban ناموفق بود.

"""

                )

                return







            username = service.get(

                "username"

            )



            link = service.get(

                "subscription"

            )



            if not link:


                link = service.get(

                    "subscription_url"

                )







            if not link:


                await query.edit_message_caption(

                    caption="""

❌ لینک اتصال ساخته نشد.

"""

                )

                return







            save_service(

                user_id,

                username,

                link,

                service.get("volume"),

                service.get("days")

            )








            await context.bot.send_message(

                chat_id=user_id,


                text=f"""

🎉 پرداخت تایید شد


━━━━━━━━━━━━


✅ سرویس شما آماده است.


👤 نام کاربری:

{username}


📦 حجم:

{service.get('volume')}


⏳ مدت:

{service.get('days')} روز


🔗 لینک اتصال:


{link}


━━━━━━━━━━━━


ممنون از اعتماد شما ❤️

"""

            )






            await query.edit_message_caption(

                caption="""

✅ پرداخت تایید شد.


✅ سرویس ساخته شد.


✅ کاربر مطلع شد.

"""

            )






        except Exception as error:



            print(

                "SERVICE ERROR:",

                error

            )



            await query.edit_message_caption(

                caption=f"""

❌ خطا:


{error}

"""

            )
            # ==========================================================
# My Service + Admin Panel
# Part 5/7
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


━━━━━━━━━━━━


👤 نام کاربری:

{service['username']}


📦 حجم:

{service['volume']}


⏳ مدت:

{service['days']} روز


🔗 لینک اتصال:


{service['subscription_url']}


━━━━━━━━━━━━

""",

        reply_markup=main_menu(user_id)

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

                "🔙 بازگشت",

                callback_data="back_home"

            )

        ]

    ]



    return InlineKeyboardMarkup(

        keyboard

    )









# ==========================================================
# Admin Panel
# ==========================================================


async def admin_panel(query):


    if query.from_user.id != ADMIN_ID:


        await query.edit_message_text(

            "❌ دسترسی ندارید."

        )

        return






    await query.edit_message_text(

        """

👑 پنل مدیریت Zeus


━━━━━━━━━━━━


مدیریت ربات

""",

        reply_markup=admin_menu()

    )









# ==========================================================
# Admin Stats
# ==========================================================


async def admin_stats(query):


    if query.from_user.id != ADMIN_ID:


        return





    stats = get_stats()





    await query.edit_message_text(

        f"""

📊 آمار ربات


━━━━━━━━━━━━


👤 کاربران:

{stats['users']}


🛒 سفارش‌ها:

{stats['orders']}


🌐 سرویس‌ها:

{stats['services']}


💰 درآمد:

{stats['income']:,} تومان


━━━━━━━━━━━━

""",

        reply_markup=admin_menu()

    )
    # ==========================================================
# Admin Orders
# Part 6/7
# ==========================================================



async def admin_orders(query):


    if query.from_user.id != ADMIN_ID:


        await query.answer(

            "❌ دسترسی ندارید",

            show_alert=True

        )

        return





    from database import get_pending_orders



    orders = get_pending_orders()





    if not orders:


        await query.edit_message_text(

            """

📦 سفارشی در انتظار نیست.

""",

            reply_markup=admin_menu()

        )

        return





    text = """

📦 سفارش‌های در انتظار


━━━━━━━━━━━━

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


━━━━━━━━━━━━

"""




    await query.edit_message_text(

        text,

        reply_markup=admin_menu()

    )









# ==========================================================
# Support Message
# ==========================================================


async def support(query):


    await query.edit_message_text(

        """

🎧 پشتیبانی Zeus


برای ارتباط با مدیریت پیام ارسال کنید.


⏰ پاسخگویی در سریع‌ترین زمان ممکن

"""

    )










# ==========================================================
# Discount Input
# ==========================================================


async def discount_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    await update.message.reply_text(

        """

🎟 کد تخفیف خود را ارسال کنید.

"""

    )


    context.user_data["waiting_discount"] = True
    # ==========================================================
# Button Handler
# Part 7/7
# ==========================================================



async def button_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data







    # =========================
    # Home
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
    # Payment
    # =========================


    if data == "payment":


        await payment_menu(

            query

        )

        return







    # =========================
    # Service
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
    # Approve / Reject
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

            button_handler

        )

    )





    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_receipt

        )

    )
    
