from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


from config import (
    BOT_TOKEN,
    ADMIN_ID,
    MARZBAN_URL
)


from order import create_order
from payment import get_payment_text
from admin import admin_buttons, create_subscription

from storage import (
    save_service,
    get_service
)

from admin_panel import admin_panel

from plans import (
    PLANS,
    get_plan
)



waiting_receipt = {}



# =========================
# منوی کاربر
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
                "🆘 پشتیبانی",
                callback_data="support"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)



# =========================
# منوی پلن ها
# =========================

def plans_keyboard():

    keyboard = []


    for key, plan in PLANS.items():

        keyboard.append(

            [

                InlineKeyboardButton(

                    text=(
                        f"📦 {plan['name']} "
                        f"| 💰 {plan['price']:,} تومان"
                    ),

                    callback_data=f"plan_{key}"

                )

            ]

        )


    return InlineKeyboardMarkup(keyboard)





# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    if user_id == ADMIN_ID:


        await update.message.reply_text(

            "👨‍💼 پنل مدیریت",

            reply_markup=admin_panel()

        )


    else:


        await update.message.reply_text(

            "🤖 ربات فروش اشتراک\n\n"
            "یکی از گزینه‌ها را انتخاب کنید:",

            reply_markup=user_menu()

        )





# =========================
# دکمه ها
# =========================

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id



    # خرید اشتراک

    if query.data == "buy":


        await query.message.reply_text(

            "📦 حجم مورد نظر را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )



    # انتخاب پلن

    elif query.data.startswith("plan_"):


        plan_id = query.data.replace(
            "plan_",
            ""
        )


        plan = get_plan(plan_id)


        if not plan:


            await query.message.reply_text(
                "❌ پلن پیدا نشد"
            )

            return



        order_id = create_order(

            user_id,

            plan["name"]

        )



        waiting_receipt[user_id] = {


            "order_id": order_id,

            "plan": plan

        }



        await query.message.reply_text(

            get_payment_text(order_id)

            +

            f"""



📦 پلن انتخابی:
{plan['name']}


💰 مبلغ:
{plan['price']:,} تومان


بعد از پرداخت، تصویر رسید را ارسال کنید.
"""

        )
        # =========================
# سرویس من
# =========================

async def my_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    service = get_service(user_id)


    if service:

        await update.message.reply_text(

            "📦 سرویس شما:\n\n"

            f"👤 نام کاربری:\n"
            f"{service['username']}\n\n"

            "🔗 لینک اشتراک:\n"

            f"{service['subscription']}"

        )


    else:

        await update.message.reply_text(
            "❌ هنوز سرویسی ندارید."
        )





# =========================
# دریافت رسید پرداخت
# =========================

async def receipt_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id


    if user_id not in waiting_receipt:

        return



    data = waiting_receipt[user_id]


    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(

            "📥 رسید پرداخت جدید\n\n"

            f"👤 کاربر:\n{user_id}\n\n"

            f"🆔 سفارش:\n{data['order_id']}\n\n"

            f"📦 پلن:\n{data['plan']['name']}"

        ),

        reply_markup=admin_buttons(
            data["order_id"]
        )

    )



    await update.message.reply_text(

        "✅ رسید شما ارسال شد.\n"
        "⏳ منتظر تایید مدیریت باشید."

    )






# =========================
# پشتیبانی
# =========================

async def support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(

        "🆘 پشتیبانی\n\n"
        "پیام خود را ارسال کنید."

    )





# =========================
# تایید و رد پرداخت
# =========================

async def approve_order(
    query,
    context
):

    order_id = query.data.replace(
        "approve_",
        ""
    )


    customer = None


    for uid, data in waiting_receipt.items():


        if data["order_id"] == order_id:

            customer = uid
            break



    if not customer:


        await query.message.reply_text(
            "❌ سفارش پیدا نشد"
        )

        return




    plan = waiting_receipt[customer]["plan"]



   
