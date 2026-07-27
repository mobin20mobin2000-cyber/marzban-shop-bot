# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 1
# ==========================================================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes
)


from config import (
    ADMIN_ID,
    CARD_NUMBER
)


from database import (
    get_user_service,
    save_receipt,
    save_support_message
)



# ==========================================================
# Main Keyboard
# ==========================================================


def main_keyboard():

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
                "💳 پرداخت",
                callback_data="payment"
            )
        ],

        [
            InlineKeyboardButton(
                "🆘 پشتیبانی",
                callback_data="support"
            )
        ]

    ]

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


    text = f"""
👑 Zeus Shop VPN PRO


سلام {user.first_name} عزیز 🌹


به ربات فروش اشتراک VPN خوش آمدید.


🚀 اتصال سریع
🔒 امن و پایدار
🌍 سرورهای قدرتمند


از منوی زیر انتخاب کنید:
"""


    await update.message.reply_text(
        text,
        reply_markup=main_keyboard()
    )



# ==========================================================
# My Service
# ==========================================================


async def my_service(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    service = get_user_service(
        user_id
    )


    if not service:

        await query.edit_message_text(
            """
❌ سرویس فعالی ندارید.


برای خرید اشتراک از بخش خرید استفاده کنید.
"""
        )

        return



    text = f"""
📦 سرویس من


👤 Username:
{service['username']}


🌐 Type:
VLESS


📅 شروع:
{service['start_date']}


📅 پایان:
{service['expire_date']}


📊 حجم:
{service['volume']} GB


✅ وضعیت:
فعال
"""


    await query.edit_message_text(
        text
    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 2
# Buy System
# ==========================================================


from database import (
    create_order,
    get_discount
)



# ==========================================================
# Plans Keyboard
# ==========================================================


def plans_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🥉 یک ماهه | 50GB",
                callback_data="plan_30"
            )
        ],

        [
            InlineKeyboardButton(
                "🥈 دو ماهه | 100GB",
                callback_data="plan_60"
            )
        ],

        [
            InlineKeyboardButton(
                "🥇 سه ماهه | 200GB",
                callback_data="plan_90"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Buy
# ==========================================================


async def buy(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query


    await query.answer()


    await query.edit_message_text(

        """
🛒 خرید اشتراک Zeus VPN


پلن مورد نظر را انتخاب کنید:
""",

        reply_markup=plans_keyboard()

    )



# ==========================================================
# Select Plan
# ==========================================================


async def select_plan(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query


    await query.answer()


    plan = query.data



    if plan == "plan_30":

        order = {
            "
            # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 3
# Payment + Support + Admin
# ==========================================================


from database import (
    get_order,
    update_order_status,
    save_service
)


from xui_api import XUI



# ==========================================================
# Payment
# ==========================================================


async def payment(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.edit_message_text(

        f"""
💳 پرداخت دستی


شماره کارت:

{CARD_NUMBER}


بعد از پرداخت،
عکس رسید را ارسال کنید.


✅ رسید توسط ادمین بررسی می‌شود.
"""

    )



# ==========================================================
# Receipt Photo
# ==========================================================


async def receipt_photo(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id


    photo = update.message.photo[-1]


    file_id = photo.file_id



    save_receipt(

        user_id,

        file_id

    )



    await update.message.reply_text(

        """
✅ رسید دریافت شد.


پس از بررسی ادمین،
سرویس شما فعال می‌شود.
"""

    )



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=file_id,

        caption=f"""
📥 رسید پرداخت جدید


👤 User ID:

{user_id}


برای تایید:

/approve {user_id}


برای رد:

/reject {user_id}
"""

    )



# ==========================================================
# Support Button
# ==========================================================


async def support(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query


    await query.answer()



    context.user_data["waiting_support"] = True



    await query.edit_message_text(

        """
🆘 پشتیبانی Zeus VPN


پیام خود را ارسال کنید.
"""

    )



# ==========================================================
# Support Message
# ==========================================================


async def support_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if not context.user_data.get(
        "waiting_support"
    ):

        return



    user_id = update.message.from_user.id


    message = update.message.text



    save_support_message(

        user_id,

        message

    )



    context.user_data["waiting_support"] = False



    await update.message.reply_text(

        """
✅ پیام شما ارسال شد.


منتظر پاسخ پشتیبانی باشید.
"""

    )



    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=f"""
🆘 پیام پشتیبانی جدید


👤 کاربر:

{user_id}


💬 پیام:

{message}
"""

    )



# ==========================================================
# Admin Approve
# ==========================================================


async def approve(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if update.effective_user.id != ADMIN_ID:

        return



    try:

        user_id = int(
            context.args[0]
        )


    except:

        await update.message.reply_text(
            "فرمت صحیح نیست."
        )

        return



    order = get_order(
        user_id
    )



    if not order:

        await update.message.reply_text(
            "❌ سفارش پیدا نشد."
        )

        return



    xui = XUI()



    result = xui.create_user(

        username=str(user_id),

        days=order["days"],

        volume=order["volume"]

    )



    if not result:

        await update.message.reply_text(
            "❌ ساخت سرویس ناموفق بود."
        )

        return



    save_service(

        user_id,

        result["link"],

        order["volume"],

        order["days"]

    )



    update_order_status(

        user_id,

        "approved"

    )



    await context.bot.send_message(

        chat_id=user_id,

        text=f"""
🎉 پرداخت تایید شد.


✅ سرویس شما فعال شد.


🔐 کانفیگ:

{result['link']}
"""

    )


    await update.message.reply_text(
        "✅ سرویس فعال شد."
    )



# ==========================================================
# Admin Reject
# ==========================================================


async def reject(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    if update.effective_user.id != ADMIN_ID:

        return



    try:

        user_id = int(
            context.args[0]
        )

    except:

        return



    update_order_status(

        user_id,

        "rejected"

    )



    await context.bot.send_message(

        chat_id=user_id,

        text="""
❌ پرداخت رد شد.


لطفاً دوباره بررسی و ارسال کنید.
"""

    )



    await update.message.reply_text(
        "❌ رسید رد شد."
            )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 4
# Register Handlers
# ==========================================================


from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)



# ==========================================================
# Text Router
# جلوگیری از تداخل پشتیبانی و تخفیف
# ==========================================================


async def text_router(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    # اگر منتظر پیام پشتیبانی است

    if context.user_data.get(
        "waiting_support"
    ):

        await support_message(
            update,
            context
        )

        return



    # اگر سفارش فعال دارد

    if "order" in context.user_data:

        await discount_handler(
            update,
            context
        )

        return



    await update.message.reply_text(

        """
❌ درخواست قابل تشخیصی نیست.

از منوی ربات استفاده کنید.
"""

    )



# ==========================================================
# Register All
# ==========================================================


def register_handlers(application):


    # --------------------------
    # Start
    # --------------------------

    application.add_handler(

        CommandHandler(
            "start",
            start
        )

    )


    # --------------------------
    # Main Buttons
    # --------------------------

    application.add_handler(

        CallbackQueryHandler(
            buy,
            pattern="^buy$"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            my_service,
            pattern="^my_service$"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            payment,
            pattern="^payment$"
        )

    )


    application.add_handler(

        CallbackQueryHandler(
            support,
            pattern="^support$"
        )

    )



    # --------------------------
    # Plans
    # --------------------------

    application.add_handler(

        CallbackQueryHandler(
            select_plan,
            pattern="^plan_"
        )

    )



    # --------------------------
    # Receipt
    # --------------------------

    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )



    # --------------------------
    # Text
    # --------------------------

    application.add_handler(

        MessageHandler(

            filters.TEXT
            &
            ~filters.COMMAND,

            text_router

        )

    )



    # --------------------------
    # Admin
    # --------------------------

    application.add_handler(

        CommandHandler(
            "approve",
            approve
        )

    )


    application.add_handler(

        CommandHandler(
            "reject",
            reject
        )

        )
