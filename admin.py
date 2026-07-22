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




def create_subscription(volume):

    marzban = Marzban()


    user = marzban.create_user(

        username=None,

        data_limit=volume * 1024 * 1024 * 1024

    )


    if user:


        return {

            "username": user.get(
                "username"
            ),

            "subscription": user.get(
                "subscription_url"
            )

        }


    return None
