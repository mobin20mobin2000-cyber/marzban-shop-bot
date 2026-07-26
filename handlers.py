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
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)


from config import (
    ADMIN_ID,
    CHANNEL_ID,
    CHANNEL_LINK
)


from texts import (
    WELCOME_TEXT,
    SUPPORT_TEXT
)


from plans import (
    PLANS,
    get_plan
)


from payment import (
    get_payment_text
)


from database import (
    add_user,
    create_order,
    last_order,
    save_subscription,
    get_subscription,
    approve_payment as db_approve_payment,
    reject_payment as db_reject_payment,
    get_stats,
    all_users,
    pending_orders,
    all_subscriptions
)


from admin import (
    admin_panel,
    admin_buttons,
    admin_dashboard,
    users_menu,
    orders_menu,
    services_menu,
    payments_menu,
    panels_menu,
    settings_menu,
    broadcast_menu,
    create_subscription,
    panel_info,
    marzban_info
)





# =========================
# بررسی عضویت کانال
# =========================

async def is_joined(
    context,
    user_id
):

    try:

        member = await context.bot.get_chat_member(

            chat_id=CHANNEL_ID,

            user_id=user_id

        )


        return member.status in [

            "member",
            "administrator",
            "creator"

        ]


    except Exception as e:

        print(
            "Join Error:",
            e
        )

        return False





# =========================
# دکمه عضویت
# =========================

def join_channel_keyboard():

    return InlineKeyboardMarkup([

        [

            InlineKeyboardButton(
                "📢 عضویت در کانال",
                url=CHANNEL_LINK
            )

        ],

        [

            InlineKeyboardButton(
                "✅ بررسی عضویت",
                callback_data="check_join"
            )

        ]

    ])
    # =========================
# منوی کاربر
# =========================

def user_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 خرید اشتراک",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "📦 سرویس من",
                callback_data="my_service"
            )
        ],

        [
            InlineKeyboardButton(
                "💬 پشتیبانی",
                callback_data="support"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )





# =========================
# منوی پلن‌ها
# =========================

def plans_keyboard():

    keyboard = []


    for key, plan in PLANS.items():

        keyboard.append(

            [

                InlineKeyboardButton(

                    f"📦 {plan['name']} | 💰 {plan['price']:,} تومان",

                    callback_data=f"plan_{key}"

                )

            ]

        )


    return InlineKeyboardMarkup(
        keyboard
    )





# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    add_user(

        user.id,

        user.username

    )



    # ادمین

    if user.id == ADMIN_ID:


        await update.message.reply_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )


        return




    # بررسی عضویت

    if not await is_joined(

        context,

        user.id

    ):


        await update.message.reply_text(

            "🔒 ابتدا عضو کانال شوید.",

            reply_markup=join_channel_keyboard()

        )


        return




    await update.message.reply_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )





# =========================
# دکمه‌های کاربر
# =========================

async def button(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id

    data = query.data




    # بررسی عضویت

    if data == "check_join":


        if await is_joined(

            context,

            user_id

        ):


            await query.message.reply_text(

                "✅ عضویت تایید شد.",

                reply_markup=user_menu()

            )


        else:

            await query.answer(

                "❌ هنوز عضو نیستید",

                show_alert=True

            )


        return





    # خرید

    if data == "buy":


        await query.message.reply_text(

            "📦 پلن را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )


        return





    # انتخاب پلن

    if data.startswith("plan_"):


        plan_id = data.replace(

            "plan_",

            ""

        )


        plan = get_plan(plan_id)



        if not plan:


            await query.message.reply_text(

                "❌ پلن پیدا نشد."

            )

            return




        order_id = create_order(

            user_id,

            plan["name"],

            plan["volume"],

            plan["days"],

            plan["price"]

        )



        await query.message.reply_text(

            get_payment_text(order_id)

            +

f"""

━━━━━━━━━━━━━━

📦 پلن:
{plan['name']}

💾 حجم:
{plan['volume']} گیگ

⏳ مدت:
{plan['days']} روز

💰 مبلغ:
{plan['price']:,} تومان

🧾 شماره سفارش:
{order_id}

━━━━━━━━━━━━━━

📸 رسید پرداخت را ارسال کنید.

"""

        )


        return
        # =========================
# نمایش سرویس من
# =========================

async def show_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    service = get_subscription(
        user_id
    )


    if not service:


        await query.message.reply_text(

            "❌ هنوز سرویس فعالی ندارید."

        )


        return



    await query.message.reply_text(

f"""
🔐 سرویس من

━━━━━━━━━━━━━━

👤 نام کاربری:
{service['marzban_username']}


🔗 لینک اتصال:
{service['subscription_url']}


📅 انقضا:
{service['expire_date'] or 'نامشخص'}

━━━━━━━━━━━━━━
"""

    )





# =========================
# پشتیبانی
# =========================

async def show_support(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query


    await query.answer()


    await query.message.reply_text(

        SUPPORT_TEXT

    )





# =========================
# دریافت رسید پرداخت
# =========================

async def receipt_photo(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    user_id = update.effective_user.id



    order = last_order(

        user_id

    )


    if not order:


        await update.message.reply_text(

            "❌ ابتدا سفارش ثبت کنید."

        )


        return




    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,


        caption=f"""

📥 رسید پرداخت جدید

━━━━━━━━━━━━━━

👤 کاربر:
{user_id}


🧾 سفارش:
{order['id']}


📦 پلن:
{order['plan']}


💾 حجم:
{order['volume']} گیگ


⏳ مدت:
{order['days']} روز


💰 مبلغ:
{order['price']:,} تومان


━━━━━━━━━━━━━━

""",

        reply_markup=admin_buttons(user_id)

    )



    await update.message.reply_text(

        """
✅ رسید دریافت شد.

⏳ منتظر تایید مدیریت باشید.
"""

    )





# =========================
# تایید پرداخت
# =========================

async def approve_payment(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return




    user_id = int(

        query.data.replace(

            "approve_",

            ""

        )

    )




    order = last_order(

        user_id

    )


    if not order:


        await query.message.reply_text(

            "❌ سفارش پیدا نشد."

        )

        return





    # ساخت سرویس مرزبان

    result = create_subscription(

        order["volume"]

    )



    if not result:


        await query.message.reply_text(

            "❌ ساخت سرویس ناموفق بود."

        )

        return





    save_subscription(

        user_id,

        order["id"],

        result["username"],

        result["subscription"],

        None

    )



    db_approve_payment(

        order["id"]

    )





    await context.bot.send_message(

        chat_id=user_id,

        text=f"""

🎉 پرداخت شما تایید شد.

━━━━━━━━━━━━━━

📦 سرویس شما آماده است.


👤 نام کاربری:

{result['username']}


🔗 لینک اشتراک:

{result['subscription']}


━━━━━━━━━━━━━━

❤️ ممنون از خرید شما

"""

    )




    await query.message.reply_text(

        "✅ سرویس ساخته شد و ارسال گردید."

    )





# =========================
# رد پرداخت
# =========================

async def reject_payment(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query


    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return




    user_id = int(

        query.data.replace(

            "reject_",

            ""

        )

    )



    order = last_order(

        user_id

    )



    if order:


        db_reject_payment(

            order["id"]

        )



        await context.bot.send_message(

            chat_id=user_id,

            text="""

❌ پرداخت شما رد شد.

در صورت نیاز دوباره رسید ارسال کنید.

"""

        )



    await query.message.reply_text(

        "❌ پرداخت رد شد."

    )
    # =========================
# پنل مدیریت
# =========================

async def admin_menu(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return



    data = query.data





    # برگشت

    if data == "admin_back":


        await query.message.edit_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )

        return





    # داشبورد

    if data == "admin_stats":


        text, keyboard = admin_dashboard()



        await query.message.edit_text(

            text,

            reply_markup=keyboard

        )

        return





    # کاربران

    if data == "admin_users":


        users = all_users()


        text = "👥 کاربران:\n\n"



        if not users:

            text += "❌ کاربری وجود ندارد."


        else:

            for user in users[:15]:


                text += f"""

🆔 {user['telegram_id']}

👤 {user['username']}

━━━━━━━━━━━━━━

"""



        await query.message.edit_text(

            text,

            reply_markup=users_menu()

        )


        return





    # سفارش‌ها

    if data == "admin_orders":


        orders = pending_orders()


        text = "📋 سفارش‌های در انتظار:\n\n"



        if not orders:

            text += "❌ سفارشی وجود ندارد."


        else:


            for order in orders[:10]:


                text += f"""

🧾 سفارش:
{order['id']}

👤 کاربر:
{order['telegram_id']}

📦 پلن:
{order['plan']}

💰 مبلغ:
{order['price']:,}

━━━━━━━━━━━━━━

"""



        await query.message.edit_text(

            text,

            reply_markup=orders_menu()

        )


        return





    # سرویس‌ها

    if data == "admin_services":


        services = all_subscriptions()


        text = "🌐 سرویس‌ها:\n\n"



        if not services:


            text += "❌ سرویسی وجود ندارد."


        else:


            for service in services[:10]:


                text += f"""

👤 کاربر:
{service['telegram_id']}

🔐 نام:
{service['marzban_username']}

━━━━━━━━━━━━━━

"""



        await query.message.edit_text(

            text,

            reply_markup=services_menu()

        )


        return





    # پرداخت‌ها

    if data == "admin_payments":


        orders = pending_orders()


        text = "💳 پرداخت‌ها:\n\n"



        if not orders:

            text += "❌ پرداختی وجود ندارد."

        else:

            for order in orders[:10]:

                text += f"""

🧾 سفارش:
{order['id']}

👤 کاربر:
{order['telegram_id']}

💰 مبلغ:
{order['price']:,}

━━━━━━━━━━━━━━

"""



        await query.message.edit_text(

            text,

            reply_markup=payments_menu()

        )


        return





    # پنل‌ها

    if data == "admin_panels":


        await query.message.edit_text(

            "🖥 مدیریت پنل‌ها",

            reply_markup=panels_menu()

        )

        return





    # تنظیمات

    if data == "settings":


        await query.message.edit_text(

            "⚙️ تنظیمات",

            reply_markup=settings_menu()

        )

        return





    # اطلاعات Marzban

    if data == "panel_marzban":


        await query.message.edit_text(

            marzban_info(),

            reply_markup=panels_menu()

        )

        return





    # پیام همگانی

    if data == "broadcast":


        await query.message.edit_text(

            "📢 پیام همگانی",

            reply_markup=broadcast_menu()

        )

        return





# =========================
# ثبت Handler ها
# =========================

def register_handlers(app):


    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    # کاربر

    app.add_handler(

        CallbackQueryHandler(

            button,

            pattern="^(buy|plan_.*|check_join)$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_service,

            pattern="^my_service$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_support,

            pattern="^support$"

        )

    )



    # پرداخت

    app.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )


    app.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

        )

    )



    # ادمین

    app.add_handler(

        CallbackQueryHandler(

            admin_menu,

            pattern="^(admin_.*|settings|broadcast|panel_.*)$"

        )

    )



    # رسید

    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )



    print(
        "✅ Zeus Shop VPN handlers loaded"
    )
