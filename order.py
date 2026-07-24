# =========================
# order.py
# Zeus Shop VPN
# =========================

import time



# =========================
# ساخت شماره سفارش
# =========================

def create_order(
    user_id,
    plan_name
):

    order_id = str(
        int(time.time())
    )


    return order_id
