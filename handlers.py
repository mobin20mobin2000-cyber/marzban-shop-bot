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

from config import (
    ADMIN_ID,
    CHANNEL_USERNAME,
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
    reject_payment as db_reject_payment
)

from admin import (
    admin_panel,
    admin_buttons,
    create_subscription
)


# =========================
# عضویت اجباری کانال
# =========================

async def is_joined(context, user_id):

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except:

        return False


def join_channel_keyboard():

    keyboard = [

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

    ]

    return InlineKeyboardMarkup(keyboard)
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

    # بررسی عضویت کانال
    if not await is_joined(
        context,
        user.id
    ):

        await update.message.reply_text(
            """
🔒 برای استفاده از ربات ابتدا باید در کانال ما عضو شوید.

بعد از عضویت روی دکمه
«✅ بررسی عضویت»
کلیک کنید.
""",
            reply_markup=join_channel_keyboard()
        )

        return

    # ورود به ربات
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=user_menu()
    )
    # =====================
# بررسی عضویت کانال
# =====================

if data == "check_join":

    if await is_joined(
        context,
        user_id
    ):

        await query.message.reply_text(
            "✅ عضویت شما تایید شد.",
            reply_markup=user_menu()
        )

    else:

        await query.answer(
            "❌ هنوز عضو کانال نشده‌اید.",
            show_alert=True
        )

    return


# =====================
# جلوگیری از استفاده بدون عضویت
# =====================

if not await is_joined(
    context,
    user_id
):

    await query.message.reply_text(
        "⚠️ ابتدا در کانال عضو شوید.",
        reply_markup=join_channel_keyboard()
    )

    return
    # خرید، پلن‌ها و بررسی عضویت

app.add_handler(

    CallbackQueryHandler(

        button,

        pattern="^(buy|plan_|check_join)"

    )

        )
