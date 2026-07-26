# =====================================
# Zeus Shop VPN
# handlers.py
# Part 1
# =====================================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes
)


from database import (
    get_user_service,
    save_receipt,
    save_support_message
)


from config import (
    ADMIN_ID,
    CARD_NUMBER
)



# =====================================
# Main Keyboard
# =====================================


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



# =====================================
# Start
# =====================================


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    user = update.effective_user


    text = f"""

👑 Zeus Shop VPN


سلام {user.first_name} عزیز 🌹


به ربات فروش اشتراک خوش آمدید.


از منوی زیر انتخاب کنید:
"""


    await update.message.reply_text(

        text,

        reply_markup=main_keyboard()

    )



# =====================================
# My Service
# =====================================


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


👤 کاربر:
{service['username']}


🌐 نوع:
VLESS


📅 تاریخ شروع:
{service['start_date']}


📅 تاریخ پایان:
{service['expire_date']}


📊 حجم:
{service['volume']} GB


✅ وضعیت:
فعال

"""


    await query.edit_message_text(
        text
    )



# =====================================
# Payment
# =====================================


async def payment(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    query = update.callback_query


    await query.answer()



    text = f"""

💳 پرداخت دستی


شماره کارت:

{CARD_NUMBER}


بعد از پرداخت،
عکس رسید را ارسال کنید.


"""


    await query.edit_message_text(
        text
    )



# =====================================
# Receive Receipt
# =====================================


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
✅ رسید شما دریافت شد.


پس از بررسی ادمین،
سرویس فعال می‌شود.
"""

    )



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=file_id,


        caption=f"""

📥 رسید پرداخت جدید


👤 کاربر:

{user_id}

"""

    )



# =====================================
# Support
# =====================================


async def support(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    await query.edit_message_text(

        """

🆘 پشتیبانی Zeus VPN


پیام خود را ارسال کنید.


"""

    )



    context.user_data["support"] = True




# =====================================
# Support Message
# =====================================


async def support_message(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "support"
    ):

        return



    user_id = update.message.from_user.id


    message = update.message.text



    save_support_message(

        user_id,

        message

    )



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
    # =====================================
# Zeus Shop VPN
# handlers.py
# Part 2
# Buy System
# =====================================


from database import (
    create_order,
    get_discount
)



# =====================================
# Plans Keyboard
# =====================================


def plans_keyboard():


    keyboard = [


        [
            InlineKeyboardButton(
                "🥉 یک ماهه - 50GB",
                callback_data="plan_30"
            )
        ],


        [
            InlineKeyboardButton(
                "🥈 دو ماهه - 100GB",
                callback_data="plan_60"
            )
        ],


        [
            InlineKeyboardButton(
                "🥇 سه ماهه - 200GB",
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



# =====================================
# Buy Button
# =====================================


async def buy(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    await query.edit_message_text(

        """

🛒 خرید اشتراک Zeus VPN


لطفاً یکی از پلن‌ها را انتخاب کنید:

""",

        reply_markup=plans_keyboard()

    )



# =====================================
# Select Plan
# =====================================


async def select_plan(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    user_id = query.from_user.id



    plan = query.data



    if plan == "plan_30":

        name = "یک ماهه"

        volume = 50

        price = 50000



    elif plan == "plan_60":

        name = "دو ماهه"

        volume = 100

        price = 90000



    elif plan == "plan_90":

        name = "سه ماهه"

        volume = 200

        price = 130000



    else:

        return




    context.user_data["order"] = {

        "name": name,

        "volume": volume,

        "price": price

    }



    text = f"""

🧾 فاکتور خرید


📦 پلن:
{name}


📊 حجم:
{volume}GB


💰 قیمت:
{price:,} تومان



اگر کد تخفیف دارید ارسال کنید.

اگر ندارید بنویسید:

ندارم

"""


    await query.edit_message_text(
        text
    )



# =====================================
# Discount Code
# =====================================


async def discount_handler(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    if "order" not in context.user_data:

        return



    code = update.message.text



    order = context.user_data["order"]



    if code == "ندارم":


        await create_final_order(

            update,

            context

        )


        return




    discount = get_discount(
        code
    )



    if discount:


        new_price = (

            order["price"]

            -

            discount

        )


        order["price"] = new_price



        await update.message.reply_text(

            f"""

✅ کد تخفیف اعمال شد.


💰 مبلغ جدید:

{new_price:,} تومان


برای پرداخت از منوی پرداخت استفاده کنید.

"""

        )



    else:


        await update.message.reply_text(

            """
❌ کد تخفیف اشتباه است.
"""

        )



# =====================================
# Create Order
# =====================================


async def create_final_order(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    user_id = update.message.from_user.id


    order = context.user_data["order"]



    order_id = create_order(

        user_id,

        order["name"],

        order["volume"],

        order["price"]

    )



    await update.message.reply_text(

        f"""

✅ سفارش ثبت شد.


🧾 شماره سفارش:

{order_id}


📦 پلن:

{order['name']}


💰 مبلغ:

{order['price']:,} تومان



اکنون پرداخت کنید و رسید را ارسال کنید.

"""

    )
    # =====================================
# Zeus Shop VPN
# handlers.py
# Part 3
# Admin Payment + Activate Service
# =====================================


from xui_api import XUI


from database import (
    get_order,
    update_order_status,
    save_service
)


from config import (
    ADMIN_ID
)



# =====================================
# Send Receipt To Admin
# =====================================


async def send_receipt_to_admin(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    user_id = update.message.from_user.id


    photo = update.message.photo[-1]


    file_id = photo.file_id



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=file_id,


        caption=f"""

📥 رسید پرداخت جدید


👤 کاربر:

{user_id}



برای تایید:

 /approve {user_id}


برای رد:

 /reject {user_id}

"""

    )



    await update.message.reply_text(

        """
✅ رسید ارسال شد.

منتظر تایید ادمین باشید.
"""

    )



# =====================================
# Admin Approve
# =====================================


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

            "فرمت اشتباه است."

        )

        return




    order = get_order(
        user_id
    )



    if not order:


        await update.message.reply_text(

            "❌ سفارشی پیدا نشد."

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

            "❌ ساخت کاربر در پنل انجام نشد."

        )

        return




    config = result["link"]



    save_service(

        user_id,

        config,

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

🎉 پرداخت شما تایید شد.


✅ سرویس شما فعال شد.


🔐 کانفیگ شما:


{config}


از خرید شما متشکریم 🌹

"""

    )



    await update.message.reply_text(

        "✅ سرویس فعال شد."

    )



# =====================================
# Admin Reject
# =====================================


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

❌ پرداخت شما رد شد.


لطفاً دوباره بررسی و ارسال کنید.

"""

    )



    await update.message.reply_text(

        "رسید رد شد."

        )
    # =====================================
# Zeus Shop VPN
# handlers.py
# Part 4
# Register Handlers
# =====================================


from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)



def register_handlers(application):


    # ==========================
    # Start
    # ==========================

    application.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    # ==========================
    # Buttons
    # ==========================


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



    # ==========================
    # Plans
    # ==========================


    application.add_handler(

        CallbackQueryHandler(

            select_plan,

            pattern="^plan_"

        )

    )



    # ==========================
    # Receipt Photo
    # ==========================


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )



    # ==========================
    # Discount / Text
    # ==========================


    application.add_handler(

        MessageHandler(

            filters.TEXT

            &

            ~filters.COMMAND,

            discount_handler

        )

    )



    # ==========================
    # Support Message
    # ==========================


    application.add_handler(

        MessageHandler(

            filters.TEXT

            &

            ~filters.COMMAND,

            support_message

        )

    )



    # ==========================
    # Admin Commands
    # ==========================


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
