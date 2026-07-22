from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID

from menus import (
    user_menu,
    plans_keyboard
)

from texts import (
    WELCOME_TEXT,
    PAYMENT_TEXT
)

from plans import get_plan

from order import create_order

from storage import (
    save_order
)


# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    if user_id == ADMIN_ID:

        from admin_panel import admin_panel

        await update.message.reply_text(
            "👨‍💼 پنل مدیریت",
            reply_markup=admin_panel()
        )

        return

    await update.message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=user_menu()
    )


# =========================
# دکمه های اصلی
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

        if not plan:

            await query.message.reply_text(

                "❌ پلن مورد نظر پیدا نشد."

            )

            return


        order_id = create_order(

            user_id,

            plan["name"]

        )


        save_order(

            order_id,

            user_id,

            plan

        )


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

        from storage import get_service

        service = get_service(user_id)

        if not service:

            await query.message.reply_text(

                "❌ هنوز هیچ سرویس فعالی برای شما ثبت نشده است."

            )

            return

        await query.message.reply_text(

            f"""📦 سرویس‌های من

━━━━━━━━━━━━━━━━━━

👤 نام کاربری:

{service['username']}

━━━━━━━━━━━━━━━━━━

🔗 لینک اشتراک:

{service['subscription']}
"""

        )

        return


    # =====================
    # پشتیبانی
    # =====================

    if data == "support":

        from texts import SUPPORT_TEXT

        await query.message.reply_text(

            SUPPORT_TEXT

        )

        return


    # =====================
    # کیف پول
    # =====================

    if data == "wallet":

        from texts import WALLET_TEXT

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

        from texts import DISCOUNT_TEXT

        await query.message.reply_text(

            DISCOUNT_TEXT

        )

        return


    # =====================
    # دعوت دوستان
    # =====================

    if data == "referral":

        from texts import REFERRAL_TEXT

        link = f"https://t.me/{context.bot.username}?start={user_id}"

        await query.message.reply_text(

            REFERRAL_TEXT.format(

                referral_link=link

            )

        )

        return


    # =====================
    # تمدید اشتراک
    # =====================

    if data == "renew":

        from texts import RENEW_TEXT

        service = None

        from storage import get_service

        service = get_service(user_id)

        if service:

            plan = "اشتراک فعال"

            expire = "در نسخه بعدی"

        else:

            plan = "ندارد"

            expire = "-"

        await query.message.reply_text(

            RENEW_TEXT.format(

                plan=plan,

                expire_date=expire

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

    from storage import get_order_by_user
    from admin import admin_buttons

    user_id = update.effective_user.id

    order = get_order_by_user(user_id)

    if not order:

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

        "✅ رسید شما با موفقیت ارسال شد.\n\n"

        "⏳ لطفاً منتظر تأیید مدیریت باشید."

    )


# =========================
# تایید پرداخت
# =========================

async def approve_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    from storage import (
        get_order,
        save_service,
        delete_order
  
