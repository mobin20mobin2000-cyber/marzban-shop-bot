from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import BOT_TOKEN, ADMIN_ID
from order import create_order


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
                "🆘 پشتیبانی",
                callback_data="support"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)



def admin_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "📋 سفارش‌ها",
                callback_data="orders"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 آمار",
                callback_data="stats"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id == ADMIN_ID:

        await update.message.reply_text(
            "👨‍💼 پنل مدیریت",
            reply_markup=admin_menu()
        )

    else:

        await update.message.reply_text(
            "🤖 به ربات فروش خوش آمدید\n\n"
            "یکی از گزینه‌ها را انتخاب کنید:",
            reply_markup=user_menu()
        )



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id


    if query.data == "buy":

        order_id = create_order(
            user_id,
            "30 روزه"
        )

        await query.message.reply_text(
            "🛒 سفارش شما ساخته شد\n\n"
            "📦 پلن: ۳۰ روزه\n"
            f"🆔 شماره سفارش:\n{order_id}\n\n"
            "💳 لطفاً مبلغ را کارت‌به‌کارت کنید."
        )


    elif query.data == "support":

        await query.message.reply_text(
            "🆘 پشتیبانی\n"
            "به زودی فعال می‌شود."
        )


    elif query.data == "my_service":

        await query.message.reply_text(
            "📦 هنوز سرویسی برای شما ثبت نشده است."
        )


    elif query.data == "orders":

        await query.message.reply_text(
            "📋 بخش سفارش‌ها در حال ساخت است."
        )


    elif query.data == "stats":

        await query.message.reply_text(
            "📊 آمار در حال ساخت است."
        )



def main():

    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )


    print(
        "Bot Started ✅"
    )


    app.run_polling()



if __name__ == "__main__":

    main()
