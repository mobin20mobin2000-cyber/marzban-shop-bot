# =========================
# handlers.py
# Zeus Shop VPN
# Part 1/4
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
    admin_panel,
    admin_buttons,
    create_subscription
)


# =========================
# منوی اصلی کاربر
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
# منوی پلن‌ها
# =========================

def plans_keyboard():

    keyboard = []

    for key, plan in PLANS.items():

        keyboard.append(

            [

                InlineKeyboardButton(

                    text=f"📦 {plan['name']} | 💰 {plan['price']:,} تومان",

                    callback_data=f"plan_{key}"

                )

            ]

        )

    return InlineKeyboardMarkup(keyboard)


# =========================
# /start
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    user_id = user.id

    # پنل مدیریت
    if user_id == ADMIN_ID:

        await update.message.reply_text(

            text="👑 به پنل مدیریت Zeus Shop VPN خوش آمدید.",

            reply_markup=admin_panel()

        )

        return

    # منوی کاربران
    await update.message.reply_text(

        text=WELCOME_TEXT,

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

            "📦 لطفاً یکی از پلن‌های زیر را انتخاب کنید:",

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
                "❌ پلن موردنظر پیدا نشد."
            )

            return

        # ایجاد شماره سفارش
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

        payment_message = (
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

📸 پس از پرداخت، تصویر رسید را ارسال کنید.
"""
        )

        await query.message.reply_text(
            payment_message
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

            "❌ هنوز هیچ سرویس فعالی ندارید."

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

    caption = f"""
📥 رسید پرداخت جدید

👤 کاربر:
{user_id}

🆔 سفارش:
{order['order_id']}

📦 پلن:
{order['plan']['name']}

💰 مبلغ:
{order['plan']['price']:,} تومان
"""

    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=caption,

        reply_markup=admin_buttons(
            order["order_id"]
        )

    )

    await update.message.reply_text(

        "✅ رسید پرداخت شما با موفقیت ارسال شد.\n\n"
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

    order_id = query.data.replace(
        "approve_",
        ""
    )

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
            "❌ خطا در ساخت سرویس در مرزبان."
        )

        return

    # ذخیره اطلاعات سرویس
    save_service(

        user_id,

        result["username"],

        result["subscription"]

    )

    # حذف سفارش
    delete_order(order_id)

    # ارسال اطلاعات به کاربر
    await context.bot.send_message(

        chat_id=user_id,

        text=(
            "🎉 پرداخت شما تایید شد.\n\n"

            "📦 سرویس شما با موفقیت ساخته شد.\n\n"

            f"👤 نام کاربری:\n"
            f"{result['username']}\n\n"

            f"🔗 لینک اشتراک:\n"
            f"{result['subscription']}"
        )

    )

    await query.message.reply_text(

        "✅ پرداخت تایید شد و سرویس برای کاربر ارسال گردید."

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
                "❌ پرداخت شما توسط
