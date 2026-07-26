# =========================
# handlers.py
# Zeus Shop VPN PRO
# =========================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    CommandHandler,
    filters
)



from config import ADMIN_ID



from database import (

    get_stats,

    all_users,

    users_count,

    all_coupons,

    create_coupon

)



from admin import (

    admin_panel,

    admin_dashboard,

    users_menu,

    orders_menu,

    payments_menu,

    services_menu,

    panels_menu,

    settings_menu,

    broadcast_menu

)
# =========================
# داشبورد ادمین
# =========================


async def show_dashboard(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    text, keyboard = admin_dashboard()



    await query.edit_message_text(

        text,

        reply_markup=keyboard

    )





# =========================
# کاربران
# =========================


async def show_users(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    count = users_count()



    text = f"""

👥 مدیریت کاربران

━━━━━━━━━━━━

تعداد کاربران:

{count}

━━━━━━━━━━━━

"""


    await query.edit_message_text(

        text,

        reply_markup=users_menu()

    )





# =========================
# لیست کاربران
# =========================


async def users_list(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    users = all_users()



    if not users:

        text = "❌ کاربری وجود ندارد"


    else:

        text = "👥 لیست کاربران:\n\n"


        for user in users[:20]:


            text += (

                f"🆔 {user['telegram_id']}\n"

                f"👤 @{user['username']}\n"

                "━━━━━━━━━━\n"

            )



    await query.edit_message_text(

        text,

        reply_markup=users_menu()

    )





# =========================
# سفارش‌ها
# =========================


async def show_orders(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    await query.edit_message_text(

        """

📋 مدیریت سفارش‌ها


از این بخش می‌توانید:

- سفارش‌های جدید را ببینید
- سفارش‌ها را مدیریت کنید
- سفارش حذف کنید


""",

        reply_markup=orders_menu()

    )
    # =========================
# پرداخت‌ها
# =========================


async def show_payments(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    text = """

💳 مدیریت پرداخت‌ها

━━━━━━━━━━━━

از این بخش می‌توانید:

⏳ پرداخت‌های در انتظار را بررسی کنید

✅ پرداخت‌ها را تایید کنید

❌ پرداخت‌ها را رد کنید

━━━━━━━━━━━━

"""



    await query.edit_message_text(

        text,

        reply_markup=payments_menu()

    )





# =========================
# سرویس‌ها
# =========================


async def show_services(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    text = """

🌐 مدیریت سرویس‌ها

━━━━━━━━━━━━

🟢 سرویس‌های فعال

⏳ سرویس‌های منقضی

🔄 تمدید سرویس

🗑 حذف سرویس

━━━━━━━━━━━━

"""



    await query.edit_message_text(

        text,

        reply_markup=services_menu()

    )





# =========================
# پنل‌ها
# =========================


async def show_panels(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    text = """

🖥 مدیریت پنل‌ها

━━━━━━━━━━━━

پنل‌های متصل:

🟢 Marzban

⚡ 3x-ui


از این بخش می‌توانید پنل جدید اضافه کنید.

━━━━━━━━━━━━

"""



    await query.edit_message_text(

        text,

        reply_markup=panels_menu()

    )
    # =========================
# تنظیمات
# =========================


async def show_settings(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    text = """

⚙️ تنظیمات ربات

━━━━━━━━━━━━

💳 تغییر شماره کارت

📢 تغییر کانال

🔗 تنظیم Marzban

━━━━━━━━━━━━

"""


    await query.edit_message_text(

        text,

        reply_markup=settings_menu()

    )





# =========================
# منوی کد تخفیف
# =========================


async def coupon_menu(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    coupons = all_coupons()



    text = """

🎟 مدیریت کد تخفیف

━━━━━━━━━━━━

"""


    if coupons:


        for coupon in coupons[:10]:


            text += (

                f"🔹 {coupon['code']}\n"

                f"💯 {coupon['percent']}٪\n"

                f"📌 استفاده: "

                f"{coupon['used']}/"

                f"{coupon['max_use']}\n"

                "━━━━━━━━━━\n"

            )


    else:


        text += "❌ هنوز کدی ساخته نشده"



    keyboard = [


        [

            InlineKeyboardButton(

                "➕ ساخت کد",

                callback_data="create_coupon"

            )

        ],


        [

            InlineKeyboardButton(

                "🔙 بازگشت",

                callback_data="admin_back"

            )

        ]

    ]



    await query.edit_message_text(

        text,

        reply_markup=InlineKeyboardMarkup(keyboard)

    )





# =========================
# شروع ساخت کد تخفیف
# =========================


async def start_coupon(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    context.user_data["create_coupon"] = True



    await query.message.reply_text(

        """

🎟 ساخت کد تخفیف


فرمت ارسال:

CODE درصد تعداد


مثال:

ZEUS20 20 100


"""

    )





# =========================
# دریافت اطلاعات کد
# =========================


async def save_coupon(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "create_coupon"
    ):

        return



    data = update.message.text.split()



    if len(data) != 3:


        await update.message.reply_text(

            "❌ فرمت اشتباه است"

        )

        return



    code = data[0]

    percent = int(data[1])

    max_use = int(data[2])



    create_coupon(

        code,

        percent,

        max_use

    )



    context.user_data["create_coupon"] = False



    await update.message.reply_text(

        "✅ کد تخفیف ساخته شد"

)
    # =========================
# منوی پیام همگانی
# =========================


async def show_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    text = """

📢 پیام همگانی

━━━━━━━━━━━━

با این بخش می‌توانید یک پیام را برای تمام کاربران ربات ارسال کنید.

روی دکمه ارسال بزنید و متن پیام را بفرستید.

━━━━━━━━━━━━

"""



    await query.edit_message_text(

        text,

        reply_markup=broadcast_menu()

    )





# =========================
# شروع ارسال پیام
# =========================


async def start_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    context.user_data["broadcast"] = True



    await query.message.reply_text(

        """

📢 متن پیام همگانی را ارسال کنید.

بعد از ارسال، پیام برای کاربران فرستاده می‌شود.

"""

    )





# =========================
# ارسال پیام به کاربران
# =========================


async def send_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "broadcast"
    ):

        return



    message = update.message.text



    users = all_users()



    success = 0



    for user in users:


        try:


            await context.bot.send_message(

                chat_id=user["telegram_id"],

                text=message

            )


            success += 1



        except Exception:


            pass



    context.user_data["broadcast"] = False



    await update.message.reply_text(

        f"""

✅ پیام همگانی ارسال شد


👥 تعداد ارسال:

{success}

"""

)
    # =========================
# ثبت Handler ها
# =========================


def register_handlers(app):


    # داشبورد

    app.add_handler(

        CallbackQueryHandler(

            show_dashboard,

            pattern="^admin_stats$"

        )

    )



    # کاربران

    app.add_handler(

        CallbackQueryHandler(

            show_users,

            pattern="^admin_users$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            users_list,

            pattern="^users_list$"

        )

    )



    # سفارش‌ها

    app.add_handler(

        CallbackQueryHandler(

            show_orders,

            pattern="^admin_orders$"

        )

    )



    # پرداخت‌ها

    app.add_handler(

        CallbackQueryHandler(

            show_payments,

            pattern="^admin_payments$"

        )

    )



    # سرویس‌ها

    app.add_handler(

        CallbackQueryHandler(

            show_services,

            pattern="^admin_services$"

        )

    )



    # پنل‌ها

    app.add_handler(

        CallbackQueryHandler(

            show_panels,

            pattern="^admin_panels$"

        )

    )



    # تنظیمات

    app.add_handler(

        CallbackQueryHandler(

            show_settings,

            pattern="^settings$"

        )

    )



    # پیام همگانی

    app.add_handler(

        CallbackQueryHandler(

            show_broadcast,

            pattern="^broadcast$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            start_broadcast,

            pattern="^send_broadcast$"

        )

    )



    # کد تخفیف

    app.add_handler(

        CallbackQueryHandler(

            coupon_menu,

            pattern="^coupon_menu$"

        )

    )


    app.add_handler(

        CallbackQueryHandler(

            start_coupon,

            pattern="^create_coupon$"

        )

    )



    # دریافت متن‌ها

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            save_coupon

        )

    )


    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            send_broadcast

        )

    )
