CARD_NUMBER = "6219861985571842"


def get_payment_text(order_id):

    return (
        "💳 پرداخت کارت‌به‌کارت\n\n"
        f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
        "📌 لطفاً مبلغ پلن را واریز کنید.\n"
        "بعد از پرداخت، عکس رسید را ارسال کنید.\n\n"
        f"🆔 شماره سفارش:\n{order_id}"
    )
