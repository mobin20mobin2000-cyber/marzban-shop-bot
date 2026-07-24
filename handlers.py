# =========================
# handlers.py
# Zeus Shop VPN
# =========================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes
)


from config import ADMIN_ID


from texts import (
    WELCOME_TEXT,
    SUPPORT_TEXT,
    MY_SERVICE_TEXT
)


from plans import (
    PLANS,
    get_plan
)


from payment import get_payment_text


from database import (
    add_user,
    create_order,
    get_order,
    save_subscription,
    get_subscription,
    approve_payment as db_approve_payment,
    reject_payment as db_reject_payment
)


from admin import (
    admin_panel,
    admin_buttons,
    create_subscription
)



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


    if user.id == ADMIN_ID:


        await update.message.reply_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )


        return



    await update.message.reply_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )
    # =========================
# مدیریت دکمه‌ها
# =========================

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id

    data = query.data



    # =========================
    # خرید اشتراک
    # =========================

    if data == "buy":

        await query.message.reply_text(

            "📦 لطفاً پلن مورد نظر را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )

        return



    # =========================
    # انتخاب پلن
    # =========================

    if data.startswith("plan_"):


        plan_id = data.replace(

            "plan_",

            ""

        )


        plan = get_plan(plan_id)


        if plan is None:


            await query.message.reply_text(

                "❌ پلن پیدا نشد."

            )

            return



        # ساخت سفارش در دیتابیس

        order_id = create_order(

            user_id,

            plan["name"],

            plan["volume"],

            30,

            plan["price"]

        )



        # ارسال اطلاعات پرداخت

        await query.message.reply_text(

            get_payment_text(

                order_id

            )

            +

            f"""



📦 پلن انتخابی:

{plan['name']}



💰 مبلغ:

{plan['price']:,} تومان



بعد از پرداخت، عکس رسید را ارسال کنید.

"""

        )


        return




    # =========================
    # پنل مدیریت
    # =========================

    if data == "admin_panel":


        if user_id != ADMIN_ID:


            await query.answer(

                "⛔ دسترسی ندارید.",

                show_alert=True

            )

            return



        await query.message.reply_text(

            "👑 پنل مدیریت",

            reply_markup=admin_panel()

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



    if service is None:


        await query.message.reply_text(

            "❌ هنوز سرویس فعالی ندارید."

        )

        return



    await query.message.reply_text(


        f"""
🔐 سرویس من

━━━━━━━━━━━━━━

👤 نام کاربری مرزبان:

{service[3]}


🔗 لینک اشتراک:

{service[4]}


📅 تاریخ انقضا:

{service[5]}


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



    photo = update.message.photo[-1]



    await context.bot.send_photo(


        chat_id=ADMIN_ID,


        photo=photo.file_id,


        caption=(

            "📥 رسید پرداخت جدید\n\n"

            f"👤 کاربر:\n{user_id}\n\n"

            "لطفاً پرداخت را بررسی کنید."

        ),


        reply_markup=admin_buttons(

            user_id

        )

    )



    await update.message.reply_text(

        """
✅ رسید شما ارسال شد.

⏳ پس از تایید مدیریت، سرویس شما ساخته می‌شود.
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



    user_id = query.data.replace(

        "approve_",

        ""

    )



    # پیدا کردن سفارش کاربر

    from database import user_orders


    orders = user_orders(

        int(user_id)

    )



    if not orders:


        await query.message.reply_text(

            "❌ سفارشی پیدا نشد."

        )

        return



    order = orders[0]



    # ساخت سرویس در مرزبان

    result = create_subscription(

        order[3]

    )



    if result is None:


        await query.message.reply_text(

            "❌ خطا در ساخت سرویس مرزبان."

        )

        return



    # ذخیره اشتراک

    save_subscription(

        int(user_id),

        order[0],

        result["username"],

        result["subscription"],

        None

    )



    # تغییر وضعیت سفارش

    db_approve_payment(

        order[0]

    )



    # ارسال برای کاربر

    await context.bot.send_message(


        chat_id=int(user_id),


        text=(

            "🎉 پرداخت شما تایید شد.\n\n"

            "📦 سرویس شما آماده است.\n\n"

            f"👤 نام کاربری:\n"

            f"{result['username']}\n\n"

            "🔗 لینک اشتراک:\n"

            f"{result['subscription']}"

        )

    )



    await query.message.reply_text(

        "✅ سرویس ساخته شد و برای کاربر ارسال گردید."

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



    user_id = query.data.replace(

        "reject_",

        ""

    )



    from database import user_orders


    orders = user_orders(

        int(user_id)

    )



    if orders:


        db_reject_payment(

            orders[0][0]

        )



    await context.bot.send_message(


        chat_id=int(user_id),


        text=(

            "❌ پرداخت شما رد شد.\n\n"

            "در صورت اشتباه، دوباره رسید ارسال کنید."

        )

    )



    await query.message.reply_text(

        "✅ پرداخت رد شد."

    )





# =========================
# ثبت Handler ها
# =========================

def register_handlers(app):


    from telegram.ext import (

        CommandHandler,

        CallbackQueryHandler,

        MessageHandler,

        filters

    )



    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            button,

            pattern="^(buy|plan_|admin_panel)$"

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



    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )
    
