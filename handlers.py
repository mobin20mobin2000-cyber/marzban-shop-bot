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
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)


from config import ADMIN_ID


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
# لیست پلن‌ها
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
# start
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



    # =====================
    # خرید اشتراک
    # =====================

    if data == "buy":


        await query.message.reply_text(

            "📦 لطفاً پلن مورد نظر را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )

        return



    # =====================
    # انتخاب پلن
    # =====================

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

📦 پلن انتخابی:

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


📸 بعد از پرداخت، عکس رسید را ارسال کنید.

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

{service["marzban_username"]}


🔗 لینک اشتراک:

{service["subscription_url"]}


📅 تاریخ انقضا:

{service["expire_date"] or "نامشخص"}

━━━━━━━━
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


    if order is None:


        await update.message.reply_text(

            "❌ ابتدا یک سفارش ثبت کنید."

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


🧾 شماره سفارش:

{order["id"]}


📦 پلن:

{order["plan"]}


💾 حجم:

{order["volume"]} گیگ


⏳ مدت:

{order["days"]} روز


💰 مبلغ:

{order["price"]:,} تومان

━━━━━━━━━━━━━━
""",


        reply_markup=admin_buttons(
            user_id
        )

    )



    await update.message.reply_text(

"""
✅ رسید شما دریافت شد.

⏳ پس از تایید مدیریت، سرویس ساخته می‌شود.
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



    if order is None:


        await query.message.reply_text(

            "❌ سفارش پیدا نشد."

        )

        return




    # ساخت کاربر در مرزبان

    result = create_subscription(

        order["volume"]

    )



    if result is None:


        await query.message.reply_text(

            "❌ خطا در ساخت سرویس مرزبان."

        )

        return




    # ذخیره سرویس

    save_subscription(

        user_id,

        order["id"],

        result["username"],

        result["subscription"],

        None

    )




    # تغییر وضعیت سفارش

    db_approve_payment(

        order["id"]

    )




    # ارسال سرویس به کاربر

    await context.bot.send_message(

        chat_id=user_id,

        text=f"""
🎉 پرداخت شما تایید شد.

━━━━━━━━━━━━━━

📦 سرویس شما آماده است.


👤 نام کاربری:

{result["username"]}


🔗 لینک اشتراک:

{result["subscription"]}


━━━━━━━━━━━━━━

❤️ ممنون از خرید شما
"""

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

در صورت اشتباه بودن، دوباره رسید ارسال کنید.
"""

        )



    await query.message.reply_text(

        "✅ پرداخت رد شد."

    )
    # =========================
# ثبت Handler ها
# =========================

def register_handlers(app):


    # دستور start

    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    # خرید و انتخاب پلن

    app.add_handler(

        CallbackQueryHandler(

            button,

            pattern="^(buy|plan_)"

        )

    )



    # سرویس من

    app.add_handler(

        CallbackQueryHandler(

            show_service,

            pattern="^my_service$"

        )

    )



    # پشتیبانی

    app.add_handler(

        CallbackQueryHandler(

            show_support,

            pattern="^support$"

        )

    )



    # تایید پرداخت

    app.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )



    # رد پرداخت

    app.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

        )

    )



    # دریافت عکس رسید

    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )


    print(
        "✅ Handlers registered successfully"
    )
