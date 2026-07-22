from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID

from menus import (
    user_menu,
    plans_keyboard
)

from texts import (
    WELCOME_TEXT,
    PAYMENT_TEXT,
    SUPPORT_TEXT,
    WALLET_TEXT,
    DISCOUNT_TEXT,
    REFERRAL_TEXT,
    RENEW_TEXT,
    MY_SERVICE_TEXT
)

from plans import get_plan
from order import create_order

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
    create_subscription
)


# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    # پنل مدیریت
    if user_id == ADMIN_ID:

        from admin_panel import admin_panel

        await update.message.reply_text(
            "👨‍💼 پنل مدیریت Zeus Shop VPN",
            reply_markup=admin_panel()
        )

        return

    # منوی کاربران
    await update.message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=user_menu()
    )


# =========================
# تابع اصلی دکمه‌ها
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

            "📦 لطفاً یکی از پلن‌های زیر را انتخاب کنید.",

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

                "❌ پلن انتخاب‌شده پیدا نشد."

            )

            return


        # ساخت شناسه سفارش
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


        # نمایش اطلاعات پرداخت
        await query.message.reply_text(

            PAYMENT_TEXT.format(

                price=plan["price"]

            )

        )

        return
            # =====================
    # سرویس‌های من
    # =====================

    if data == "my_service":

        service = get_service(user_id)

        if not service:

            await query.message.reply_text(
                "❌ هنوز هیچ سرویس فعالی برای شما ثبت نشده است."
            )
            return

        await query.message.reply_text(

            MY_SERVICE_TEXT.format(

                username=service["username"],

                subscription=service["subscription"]

            )

        )

        return


    # =====================
    # پشتیبانی
    # =====================

    if data == "support":

        await query.message.reply_text(
            SUPPORT_TEXT
        )

        return


    # =====================
    # کیف پول
    # =====================

    if data == "wallet":

        balance = 0

        await query.message.reply_text(

            WALLET_TEXT.format(

                balance=balance

            )

        )

        return


    # =====================
    # کد تخفیف
    # =====================

    if data == "discount":

        await query.message.reply_text(

            DISCOUNT_TEXT

        )

        return


    # =====================
    # دعوت دوستان
    # =====================

    if data == "referral":

        bot_username = (await context.bot.get_me()).username

        referral_link = (

            f"https://t.me/{bot_username}?start={user_id}"

        )

        await query.message.reply_text(

            REFERRAL_TEXT.format(

                referral_link=referral_link

            )

        )

        return


    # =====================
    # تمدید اشتراک
    # =====================

    if data == "renew":

        service = get_service(user_id)

        if service:

            plan_name = "اشتراک فعال"

            expire_date = "به‌زودی"

        else:

            plan_name = "ندارد"

            expire_date = "-"

        await query.message.reply_text(

            RENEW_TEXT.format(

                plan=plan_name,

                expire_date=expire_date

            )

        )

        return
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

            "❌ ابتدا یک سفارش ایجاد کنید."

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

    result = create_subscription(

        order["plan"]["volume"]

    )

    if result is None:

        await query.message.reply_text(

            "❌ ساخت سرویس با خطا مواجه شد."

        )

        return

    save_service(

        order["user_id"],

        result["username"],

        result["subscription"]

    )

    delete_order(order_id)

    await context.bot.send_message(

        chat_id=order["user_id"],

        text=(

            "🎉 پرداخت شما تأیید شد.\n\n"

            f"👤 نام کاربری:\n"

            f"{result['username']}\n\n"

            f"🔗 لینک اشتراک:\n"

            f"{result['subscription']}"

        )

    )

    await query.message.reply_text(

       
    "✅ سرویس با موفقیت ساخته شد و برای کاربر ارسال گردید."

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
                "در صورت نیاز، لطفاً پس از بررسی مجدداً رسید پرداخت را ارسال کنید یا با پشتیبانی تماس بگیرید."
            )

        )

    await query.message.reply_text(

        "✅ سفارش رد شد."

    )


# =========================
# کانال
# =========================

async def show_channel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(

        "📢 کانال رسمی Zeus Shop VPN\n\n"
        "https://t.me/YOUR_CHANNEL"

    )


# =========================
# راهنما
# =========================

async def show_help(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(

        """ℹ️ راهنمای استفاده

1️⃣ خرید اشتراک را انتخاب کنید.

2️⃣ پلن مورد نظر را انتخاب کنید.

3️⃣ مبلغ را کارت‌به‌کارت واریز کنید.

4️⃣ تصویر رسید را ارسال نمایید.

5️⃣ پس از تأیید مدیریت، سرویس به صورت خودکار برای شما ارسال خواهد شد.

🛠 در صورت بروز هرگونه مشکل، از بخش «پشتیبانی» با ما در ارتباط باشید.
"""

    )


# =========================
# پایان فایل handlers.py
# =========================
