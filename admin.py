from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from marzban import Marzban



def admin_buttons(order_id):

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ تأیید پرداخت",
                callback_data=f"approve_{order_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ رد پرداخت",
                callback_data=f"reject_{order_id}"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)



def create_subscription():

    marzban = Marzban()


    user = marzban.create_user(
        username=None,
        days=30
    )


    if user:

        username = user.get(
            "username"
        )


        sub = (
            user.get(
                "subscription_url"
            )
        )


        return {
            "username": username,
            "subscription": sub
        }


    return None
