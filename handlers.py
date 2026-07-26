# =========================
# handlers.py
# Zeus Shop VPN PRO
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

    reject_payment as db_reject_payment,

    get_stats,

    all_users,

    pending_orders,

    all_subscriptions,

    create_coupon,

    all_coupons,

    get_coupon,

    use_coupon

)


from admin import (

    admin_panel,

    admin_buttons,

    users_menu,

    orders_menu,

    services_menu,

    payments_menu,

    panels_menu,

    settings_menu,

    coupons_menu,

    coupons_list_text,

    broadcast_menu,

    create_subscription

)
# =========================
# منوی کاربر
# =========================


def user_menu():


    return InlineKeyboardMarkup([


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
                "🎟 کد تخفیف",
                callback_data="enter_coupon"
            )

        ],


        [

            InlineKeyboardButton(
                "💬 پشتیبانی",
                callback_data="support"
            )

        ]

    ])





# =========================
# منوی پلن‌ها
# =========================


def plans_keyboard():


    keyboard = []



    for key, plan in PLANS.items():


        keyboard.append([


            InlineKeyboardButton(

                f"📦 {plan['name']} | 💰 {plan['price']:,} تومان",

                callback_data=f"plan_{key}"

            )

        ])



    return InlineKeyboardMarkup(
        keyboard
    )





# =========================
# بررسی کد تخفیف
# =========================


def check_coupon(
    code,
    price
):


    coupon = get_coupon(
        code
    )


    if not coupon:

        return price



    # اگر تعداد استفاده تمام شده

    if coupon["used"] >= coupon["max_use"]:

        return price




    discount = (

        price *

        coupon["percent"]

        //

        100

    )



    new_price = price - discount



    return new_price
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



    if user.id == ADMIN_ID:


        await update.message.reply_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )


        return




    await update.message.reply_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )





# =========================
# دکمه‌های اصلی کاربر
# =========================


async def button(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    user_id = query.from_user.id


    data = query.data




    # خرید


    if data == "buy":


        await query.message.reply_text(

            "📦 پلن مورد نظر را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )


        return






    # وارد کردن کد تخفیف


    if data == "enter_coupon":


        context.user_data["waiting_coupon"] = True



        await query.message.reply_text(

            """
🎟 کد تخفیف خود را ارسال کنید:

مثال:
ZEUS20
"""

        )


        return





    # انتخاب پلن


    if data.startswith("plan_"):


        plan_id = data.replace(

            "plan_",

            ""

        )



        plan = get_plan(
            plan_id
        )



        if not plan:


            await query.message.reply_text(

                "❌ پلن پیدا نشد."

            )


            return





        price = plan["price"]



        coupon = context.user_data.get(
            "coupon"
        )



        if coupon:


            price = check_coupon(

                coupon,

                price

            )



            use_coupon(
                coupon
            )





        order_id = create_order(

            user_id,

            plan["name"],

            plan["volume"],

            plan["days"],

            price,

            coupon

        )





        await query.message.reply_text(

f"""
🧾 سفارش شما ثبت شد

━━━━━━━━━━━━━━

📦 پلن:
{plan['name']}

💾 حجم:
{plan['volume']} گیگ

⏳ مدت:
{plan['days']} روز

💰 مبلغ:
{price:,} تومان

🧾 شماره سفارش:
{order_id}

━━━━━━━━━━━━━━

📸 بعد از پرداخت عکس رسید را ارسال کنید.
"""

        )


        return





# =========================
# دریافت کد تخفیف
# =========================


async def coupon_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "waiting_coupon"
    ):

        return



    code = update.message.text.strip()



    coupon = get_coupon(
        code
    )



    if not coupon:


        await update.message.reply_text(

            "❌ کد تخفیف اشتباه است."

        )


        return





    context.user_data["coupon"] = code

    context.user_data["waiting_coupon"] = False




    await update.message.reply_text(

f"""
✅ کد تخفیف فعال شد

🎟 کد:
{code}

💯 تخفیف:
{coupon['percent']}٪

اکنون می‌توانید خرید کنید.
"""

)
    # =========================
# دریافت رسید پرداخت
# =========================


async def receipt_photo(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user_id = update.effective_user.id



    order = last_order(
        user_id
    )



    if not order:


        await update.message.reply_text(

            "❌ ابتدا سفارش ثبت کنید."

        )


        return




    photo = update.message.photo[-1]




    await context.bot.send_photo(

        chat_id=ADMIN_ID,


        photo=photo.file_id,


        caption=f"""

📥 رسید پرداخت جدید

━━━━━━━━━━━━━━

👤 کاربر:

{user_id}


🧾 سفارش:

{order['id']}


📦 پلن:

{order['plan']}


💾 حجم:

{order['volume']} گیگ


💰 مبلغ:

{order['price']:,} تومان


━━━━━━━━━━━━━━

""",


        reply_markup=admin_buttons(
            user_id
        )

    )




    await update.message.reply_text(

"""
✅ رسید دریافت شد.

⏳ منتظر تایید مدیریت باشید.
"""

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



    if query.from_user.id != ADMIN_ID:

        return



    user_id = int(

        query.data.replace(

            "approve_",

            ""

        )

    )



    order = last_order(
        user_id
    )



    if not order:


        await query.message.reply_text(

            "❌ سفارش پیدا نشد."

        )


        return





    result = create_subscription(

        order["volume"]

    )



    if not result:


        await query.message.reply_text(

            "❌ ساخت سرویس ناموفق بود."

        )


        return





    save_subscription(

        user_id,

        order["id"],

        result["username"],

        result["subscription"],

        None

    )




    db_approve_payment(

        order["id"]

    )





    await context.bot.send_message(

        chat_id=user_id,


        text=f"""

🎉 پرداخت تایید شد

━━━━━━━━━━━━━━

👤 نام کاربری:

{result['username']}


🔗 لینک اشتراک:

{result['subscription']}


━━━━━━━━━━━━━━

ممنون از خرید شما ❤️

"""

    )





    await query.message.reply_text(

        "✅ سرویس ساخته شد و ارسال گردید."

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



    if query.from_user.id != ADMIN_ID:

        return




    user_id = int(

        query.data.replace(

            "reject_",

            ""

        )

    )




    order = last_order(
        user_id
    )



    if order:


        db_reject_payment(

            order["id"]

        )



        await context.bot.send_message(

            chat_id=user_id,


            text="""

❌ پرداخت شما رد شد.

در صورت اشتباه دوباره رسید ارسال کنید.

"""

        )




    await query.message.reply_text(

        "✅ پرداخت رد شد."

    )
    # =========================
# پنل مدیریت
# =========================


async def admin_menu(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return



    data = query.data





    # بازگشت

    if data == "admin_back":


        await query.message.edit_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )


        return





    # داشبورد

    if data == "admin_stats":


        stats = get_stats()



        text = f"""

📊 داشبورد Zeus Shop VPN

━━━━━━━━━━━━━━

👥 کاربران:
{stats['users']}


🛒 فروش:
{stats['sales']}


💰 درآمد:
{stats['income']:,} تومان


🌐 سرویس فعال:
{stats['subscriptions']}


⏳ پرداخت در انتظار:
{stats.get('pending',0)}

━━━━━━━━━━━━━━

"""



        await query.message.edit_text(

            text,

            reply_markup=admin_panel()

        )


        return






    # کاربران

    if data == "admin_users":


        users = all_users()



        text = "👥 کاربران اخیر:\n\n"



        for user in users[:20]:


            text += f"""

🆔 {user['telegram_id']}

👤 {user['username']}

━━━━━━━━

"""



        await query.message.edit_text(

            text,

            reply_markup=users_menu()

        )


        return






    # کد تخفیف

    if data == "admin_coupons":


        await query.message.edit_text(

            "🎟 مدیریت کد تخفیف",

            reply_markup=coupons_menu()

        )


        return






    # لیست کدها

    if data == "list_coupons":


        await query.message.edit_text(

            coupons_list_text(),

            reply_markup=coupons_menu()

        )


        return






    # پیام همگانی

    if data == "broadcast":


        context.user_data["broadcast"] = True



        await query.message.reply_text(

            """
📢 پیام همگانی

متن پیام را ارسال کنید.
"""

        )


        return
        # =========================
# پیام همگانی
# =========================


async def broadcast_message(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "broadcast"
    ):

        return



    text = update.message.text



    users = all_users()



    count = 0



    for user in users:


        try:


            await context.bot.send_message(

                chat_id=user["telegram_id"],

                text=text

            )


            count += 1



        except Exception as e:


            print(
                "Broadcast Error:",
                e
            )



    context.user_data["broadcast"] = False



    await update.message.reply_text(

f"""
✅ پیام همگانی ارسال شد

👥 تعداد ارسال:
{count}

"""

    )





# =========================
# ساخت کد تخفیف توسط ادمین
# =========================


async def create_coupon_admin(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if update.effective_user.id != ADMIN_ID:

        return



    context.user_data["create_coupon"] = True



    await update.message.reply_text(

"""
🎟 ساخت کد تخفیف

فرمت ارسال:

CODE درصد تعداد

مثال:

ZEUS20 20 100

"""

    )





async def coupon_create_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(
        "create_coupon"
    ):

        return



    data = update.message.text.split()



    if len(data) != 3:


        await update.message.reply_text(

            "❌ فرمت اشتباه است."

        )


        return




    code = data[0]

    percent = int(data[1])

    max_use = int(data[2])



    create_coupon(

        code,

        percent,

        max_use

    )



    context.user_data["create_coupon"] = False



    await update.message.reply_text(

f"""
✅ کد تخفیف ساخته شد

🎟 کد:
{code}

💯 درصد:
{percent}٪

📌 تعداد:
{max_use}

"""

    )







# =========================
# ثبت Handler ها
# =========================


def register_handlers(app):



    # شروع

    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )




    # دکمه‌ها

    app.add_handler(

        CallbackQueryHandler(

            button

        )

    )



    # پنل ادمین

    app.add_handler(

        CallbackQueryHandler(

            admin_menu

        )

    )



    # تایید پرداخت

    app.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )



    # رد پرداخت

    app.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

        )

    )



    # عکس رسید

    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )



    # پیام همگانی

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            broadcast_message

        )

    )



    # ساخت کد تخفیف

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            coupon_create_handler

        )

    )



    print(
        "✅ Handlers Loaded"
        )
