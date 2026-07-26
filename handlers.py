# =========================
# handlers.py
# Zeus Shop VPN PRO
# =========================


from telegram import Update


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
    create_coupon,
    all_coupons
)
# =========================
# بررسی ادمین
# =========================

def is_admin(user_id):

    return user_id == ADMIN_ID





# =========================
# باز کردن پنل ادمین
# =========================


async def admin_start(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    user_id = update.effective_user.id



    if not is_admin(user_id):

        return



    await update.message.reply_text(

        "👑 پنل مدیریت Zeus Shop VPN",

        reply_markup=admin_panel()

    )





# =========================
# داشبورد
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



    await query.edit_message_text(

        f"""

👥 مدیریت کاربران


تعداد کاربران:

{users_count()}

""",

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

━━━━━━━━━━

مدیریت سفارش‌های کاربران

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



    await query.edit_message_text(

        """

💳 مدیریت پرداخت‌ها

━━━━━━━━━━

بررسی و تایید پرداخت‌ها

""",

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



    await query.edit_message_text(

        """

🌐 مدیریت سرویس‌ها

━━━━━━━━━━

مدیریت اشتراک کاربران

""",

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



    await query.edit_message_text(

        """

🖥 مدیریت پنل‌ها

━━━━━━━━━━

Marzban / 3x-ui

""",

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



    await query.edit_message_text(

        """

⚙️ تنظیمات ربات

━━━━━━━━━━

مدیریت تنظیمات اصلی ربات

""",

        reply_markup=settings_menu()

    )





# =========================
# کد تخفیف
# =========================


async def show_coupons(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    coupons = all_coupons()



    text = """

🎟 کدهای تخفیف

━━━━━━━━━━

"""



    if coupons:


        for c in coupons:


            text += (

                f"🔹 {c['code']}\n"

                f"💯 درصد: {c['percent']}٪\n"

                f"📌 استفاده: "

                f"{c['used']}/{c['max_use']}\n\n"

            )


    else:


        text += "❌ کدی وجود ندارد"



    await query.edit_message_text(

        text,

        reply_markup=coupon_menu()

    )





# =========================
# ساخت کد تخفیف
# =========================


async def create_coupon_start(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    context.user_data["coupon_create"] = True



    await query.message.reply_text(

        """

🎟 ساخت کد تخفیف


فرمت:

CODE درصد تعداد


مثال:

ZEUS20 20 50

"""

    )





async def receive_coupon(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "coupon_create"
    ):

        return



    data = update.message.text.split()



    if len(data) != 3:


        await update.message.reply_text(

            "❌ فرمت اشتباه"

        )

        return



    create_coupon(

        data[0],

        int(data[1]),

        int(data[2])

    )



    context.user_data["coupon_create"] = False



    await update.message.reply_text(

        "✅ کد تخفیف ساخته شد"

    )





# =========================
# پیام همگانی
# =========================


async def show_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    await query.edit_message_text(

        """

📢 پیام همگانی

━━━━━━━━━━

متن پیام را ارسال کنید.

""",

        reply_markup=broadcast_menu()

    )





async def start_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    context.user_data["broadcast"] = True



    await query.message.reply_text(

        "📢 پیام خود را ارسال کنید"

    )





async def send_broadcast(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "broadcast"
    ):

        return



    text = update.message.text



    users = all_users()



    count = 0



    for user in users:


        try:


            await context.bot.send_message(

                chat_id=user["telegram_id"],

                text=text

            )


            count += 1


        except:


            pass



    context.user_data["broadcast"] = False



    await update.message.reply_text(

        f"""

✅ پیام همگانی ارسال شد

👥 تعداد ارسال:

{count}

"""

        )
    
# =========================
# بازگشت به پنل ادمین
# =========================


async def admin_back(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    await query.edit_message_text(

        "👑 پنل مدیریت Zeus Shop VPN",

        reply_markup=admin_panel()

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


        text = "❌ هیچ کاربری وجود ندارد"


    else:


        text = "👥 لیست کاربران:\n\n"



        for user in users[:30]:


            username = user["username"] or "-"



            text += (

                f"🆔 {user['telegram_id']}\n"

                f"👤 {username}\n"

                "━━━━━━━━━━\n"

            )



    await query.edit_message_text(

        text,

        reply_markup=users_menu()

    )





# =========================
# سفارش‌های در انتظار
# =========================


async def pending_orders(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    from database import pending_orders



    query = update.callback_query

    await query.answer()



    orders = pending_orders()



    if not orders:


        text = "⏳ سفارشی در انتظار نیست"


    else:


        text = "⏳ سفارش‌های در انتظار:\n\n"



        for order in orders:


            text += (

                f"🆔 سفارش: {order['id']}\n"

                f"👤 کاربر: {order['telegram_id']}\n"

                f"💰 قیمت: {order['price']}\n"

                "━━━━━━━━━━\n"

            )



    await query.edit_message_text(

        text,

        reply_markup=orders_menu()

    )





# =========================
# تایید پرداخت
# =========================


async def approve_order(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    from database import approve_payment



    query = update.callback_query

    await query.answer()



    order_id = int(

        query.data.split("_")[1]

    )



    approve_payment(

        order_id

    )



    await query.edit_message_text(

        "✅ پرداخت تایید شد"

    )





# =========================
# رد پرداخت
# =========================


async def reject_order(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    from database import reject_payment



    query = update.callback_query

    await query.answer()



    order_id = int(

        query.data.split("_")[1]

    )



    reject_payment(

        order_id

    )



    await query.edit_message_text(

        "❌ پرداخت رد شد"

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
    coupon_menu,
    broadcast_menu
)
# =========================
# پنل Marzban
# =========================


async def panel_marzban(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    from admin import marzban_info



    await query.edit_message_text(

        marzban_info(),

        reply_markup=panels_menu()

    )





# =========================
# تست اتصال پنل
# =========================


async def test_panel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    from admin import test_marzban



    status = test_marzban()



    if status:


        text = """

🟢 اتصال Marzban موفق است

"""

    else:


        text = """

🔴 اتصال Marzban ناموفق است

"""



    await query.edit_message_text(

        text,

        reply_markup=panels_menu()

    )





# =========================
# سرویس‌های فعال
# =========================


async def active_services(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    from database import all_subscriptions



    services = all_subscriptions()



    text = """

🌐 سرویس‌های فعال

━━━━━━━━━━

"""



    if not services:


        text += "❌ سرویسی وجود ندارد"


    else:


        for s in services:


            text += (

                f"👤 {s['telegram_id']}\n"

                f"🔗 {s['subscription_url']}\n"

                "━━━━━━━━━━\n"

            )



    await query.edit_message_text(

        text,

        reply_markup=services_menu()

    )





# =========================
# سرویس‌های منقضی
# =========================


async def expired_services(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()



    await query.edit_message_text(

        """

⏳ سرویس‌های منقضی

فعلا بررسی تاریخ انقضا فعال نشده است.

""",

        reply_markup=services_menu()

    )
    # =========================
# ثبت همه Handler ها
# =========================


def register_handlers(app):


    # =====================
    # فرمان ادمین
    # =====================


    app.add_handler(

        CommandHandler(

            "admin",

            admin_start

        )

    )



    # =====================
    # منوهای اصلی ادمین
    # =====================


    app.add_handler(

        CallbackQueryHandler(

            show_dashboard,

            pattern="^admin_stats$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_users,

            pattern="^admin_users$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_orders,

            pattern="^admin_orders$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_payments,

            pattern="^admin_payments$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_services,

            pattern="^admin_services$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_panels,

            pattern="^admin_panels$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_settings,

            pattern="^settings$"

        )

    )



    # =====================
    # برگشت
    # =====================


    app.add_handler(

        CallbackQueryHandler(

            admin_back,

            pattern="^admin_back$"

        )

    )



    # =====================
    # کاربران
    # =====================


    app.add_handler(

        CallbackQueryHandler(

            users_list,

            pattern="^users_list$"

        )

    )



    # =====================
    # کد تخفیف
    # =====================


    app.add_handler(

        CallbackQueryHandler(

            show_coupons,

            pattern="^coupon_menu$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            create_coupon_start,

            pattern="^create_coupon$"

        )

    )



    # =====================
    # پیام همگانی
    # =====================


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



    # =====================
    # سفارش و پرداخت
    # =====================


    app.add_handler(

        CallbackQueryHandler(

            pending_orders,

            pattern="^pending_orders$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            approve_order,

            pattern="^approve_"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            reject_order,

            pattern="^reject_"

        )

    )



    # =====================
    # پنل ها
    # =====================


    app.add_handler(

        CallbackQueryHandler(

            panel_marzban,

            pattern="^panel_marzban$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            test_panel,

            pattern="^test_panel$"

        )

    )



    # =====================
    # دریافت متن
    # =====================


    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            receive_coupon

        )

    )


    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            send_broadcast

        )

    )
