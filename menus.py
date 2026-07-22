from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from plans import PLANS


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
                "📦 سرویس‌های من",
                callback_data="my_service"
            )
        ],

        [
            InlineKeyboardButton(
                "⭐ تمدید اشتراک",
                callback_data="renew"
            ),
            InlineKeyboardButton(
                "💳 کیف پول",
                callback_data="wallet"
            )
        ],

        [
            InlineKeyboardButton(
                "🎁 کد تخفیف",
                callback_data="discount"
            ),
            InlineKeyboardButton(
                "👥 دعوت دوستان",
                callback_data="referral"
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


def plans_keyboard():

    keyboard = []

    for key, plan in PLANS.items():

        keyboard.append([

            InlineKeyboardButton(

                f"📦 {plan['name']} | 💰 {plan['price']:,} تومان",

                callback_data=f"plan_{key}"

            )

        ])

    return InlineKeyboardMarkup(keyboard)
