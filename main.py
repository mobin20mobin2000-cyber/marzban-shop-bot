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
    PAYMENT_TEXT,
    SUPPORT_TEXT,
    MY_SERVICE_TEXT
)

from plans import (
    PLANS,
    get_plan
)

from order import (
    create_order
)

from storage import (
    save_order,
    get_order,
    get_order_by_user,
    delete_order,
    save_service,
    get_service
)

from admin import (
    admin_buttons,
    create_subscription,
    admin_panel
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

    return InlineKeyboardMarkup(keyboard)


# =========================
# منوی پلن ها
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

    return InlineKeyboardMarkup(keyboard)


# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    # ادمین

    if user_id == ADMIN_ID:

        await update.message.reply_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )

        return

    # کاربر

    await update.message.reply_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )


# =========================
# مدیریت دکمه ها
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
    # پنل مدیریت
    # =====================

    if data == "admin_panel":

        if user_id != ADMIN_ID:

            await query.answer(
                "⛔ دسترسی ندارید.",
                show_alert=True
            )

            return

        await query.message.reply_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )

        return


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

        # ایجاد سفارش
        order_id = create_order(
            user_id,
            plan["name"]
        )

        # ذخیره سفارش
        save_order(
            order_id,
            user_id,
            plan
        )

        await query.message.reply_text(

            PAYMENT_TEXT.format(
                price=plan["price"]
            )

            +

            f"""

🧾 شماره سفارش:
{order_id}

📦 پلن:
{plan['name']}

💰 مبلغ:
{plan['price']:,} تومان

بعد از پرداخت، عکس رسید را ارسال کنید.

"""

        )

        return
       # =========================
# سرویس من
# =========================

async def show_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    service = get_service(user_id)

    if service is None:

        await query.message.reply_text(
            "❌ هنوز سرویس فعالی ندارید."
        )

        return

    await query.message.reply_text(

        MY_SERVICE_TEXT.format(

            username=service["username"],

            subscription=service["subscription"]

        )

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

    order = get_order_by_user(user_id)

    if order is None:

        await update.message.reply_text(

            "❌ ابتدا یک سفارش ثبت کنید."

        )

        return

    photo = update.message.photo[-1]

    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(

            "📥 رسید پرداخت جدید\n\n"

            f"👤 کاربر: {user_id}\n"

            f"🆔 سفارش: {order['order_id']}\n"

            f"📦 پلن: {order['plan']['name']}\n"

            f"💰 مبلغ: {order['plan']['price']:,} تومان"

        ),

        reply_markup=admin_buttons(
            order["order_id"]
        )

    )

    await update.message.reply_text(

        "✅ رسید پرداخت شما ارسال شد.\n\n"

        "⏳ لطفاً منتظر تأیید مدیریت باشید."

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

    order_id = query.data.replace("approve_", "")

    order = get_order(order_id)

    if order is None:

        await query.message.reply_text(
            "❌ سفارش پیدا نشد."
        )

        return

    user_id = order["user_id"]
    plan = order["plan"]

    # ساخت سرویس در مرزبان
    result = create_subscription(
        plan["volume"]
    )

    if result is None:

        await query.message.reply_text(
            "❌ خطا در ساخت سرویس."
        )

        return

    # ذخیره سرویس
    save_service(

        user_id,

        result["username"],

        result["subscription"]

    )

    # حذف سفارش
    delete_order(order_id)

    # ارسال سرویس برای کاربر
    await context.bot.send_message(

        chat_id=user_id,

        text=(
            "🎉 پرداخت شما تایید شد.\n\n"

            "📦 سرویس شما آماده است.\n\n"

            f"👤 نام کاربری:\n{result['username']}\n\n"

            f"🔗 لینک اشتراک:\n{result['subscription']}"
        )

    )

    await query.message.reply_text(

        "✅ سرویس با موفقیت ساخته و ارسال شد."

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

    order_id = query.data.replace(
        "reject_",
        ""
    )

    order = get_order(order_id)

    if order:

        delete_order(order_id)

        await context.bot.send_message(

            chat_id=order["user_id"],

            text=(
                "❌ پرداخت شما توسط مدیریت رد شد.\n\n"

                "در صورت نیاز دوباره رسید ارسال کنید."
            )

        )

    await query.message.reply_text(

        "✅ سفارش رد شد."

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

    # start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # خرید و پنل مدیریت
    app.add_handler(
        CallbackQueryHandler(
            button,
            pattern="^(buy|plan_|admin_panel)$"
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

    # رسید پرداخت
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receipt_photo
        )
        )
