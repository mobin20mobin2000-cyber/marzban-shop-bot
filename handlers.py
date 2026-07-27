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
    create_order,
    last_order,
    save_receipt,
    get_user_service,
    save_service
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



    # فقط ادمین ببیند

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



    text=f"""

👑 Zeus Shop VPN


سلام {user.first_name} 🌹


به ربات رسمی خرید VPN خوش آمدید.


🚀 اینترنت پرسرعت
🔐 اتصال امن
⚡ فعالسازی سریع


از منوی زیر انتخاب کنید 👇

"""



    await update.message.reply_text(

        text,

        reply_markup=main_menu(user.id)

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

ابتدا خرید انجام دهید.
""",

            reply_markup=main_menu(
                query.from_user.id
            )

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


بعد از پرداخت عکس رسید را ارسال کنید.

"""


    )
    # ==========================================================
# Receipt Handler
# Part 3/5
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
# Payment Approval
# ==========================================================


async def payment_action(

    query,

    context

):


    data = query.data





    # =========================
    # Approve
    # =========================


    if data.startswith("approve_"):


        user_id = int(

            data.split("_")[1]

        )



        try:



            marzban = Marzban()



            service = marzban.create_service(

                volume=50,

                days=30

            )





            if service:




                save_service(


                    user_id,


                    service["username"],


                    service["subscription_url"],


                    service["volume"],


                    service["days"]

                )





                await context.bot.send_message(


                    chat_id=user_id,


                    text=f"""

🎉 سرویس شما فعال شد


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


ممنون از اعتماد شما ❤️

"""

                )





                await query.edit_message_caption(

                    caption="""

✅ پرداخت تایید شد


✅ سرویس ساخته شد


✅ برای کاربر ارسال شد.

"""

                )





            else:



                await query.edit_message_caption(

                    caption="""

❌ پرداخت تایید شد

ولی ساخت سرویس Marzban ناموفق بود.

"""

                )





        except Exception as error:


            print(

                "SERVICE ERROR:",

                error

            )



            await query.edit_message_caption(

                caption=f"""

❌ خطا در ساخت سرویس:


{error}

"""

            )



        return







    # =========================
    # Reject
    # =========================


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

❌ پرداخت
        # ==========================================================
# My Service
# Part 4/5
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


"""

,

        reply_markup=main_menu(user_id)

    )









# ==========================================================
# Admin Menu
# ==========================================================


def admin_menu():


    keyboard = [


        [

            InlineKeyboardButton(

                "📊 آمار کاربران",

                callback_data="admin_stats"

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

                "🔙 برگشت",

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


async def admin_panel(

    query

):


    if query.from_user.id != ADMIN_ID:


        await query.edit_message_text(

            "❌ دسترسی ندارید."

        )

        return





    await query.edit_message_text(


        """

👑 پنل مدیریت Zeus


━━━━━━━━━━━━


از گزینه‌های زیر استفاده کنید.

""",


        reply_markup=admin_menu()

    )









# ==========================================================
# Admin Stats
# ==========================================================


async def admin_stats(

    query

):


    if query.from_user.id != ADMIN_ID:

        return





    from database import get_stats



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


        await query.edit_message_text(

            """

🎧 پشتیبانی


برای ارتباط با مدیریت پیام ارسال کنید.

"""

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





    # =========================
    # Approve / Reject
    # =========================


    if data.startswith("approve_") or data.startswith("reject_"):


        if query.from_user.id != ADMIN_ID:


            return



        await payment_action(

            query,

            context

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
