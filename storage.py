# =========================
# سرویس کاربران
# =========================

services = {}

def save_service(user_id, username, subscription):

    services[user_id] = {
        "username": username,
        "subscription": subscription
    }


def get_service(user_id):

    return services.get(user_id)


# =========================
# سفارش‌ها
# =========================

orders = {}


def save_order(order_id, user_id, plan):

    orders[order_id] = {
        "order_id": order_id,
        "user_id": user_id,
        "plan": plan
    }


def get_order(order_id):

    return orders.get(order_id)


def get_order_by_user(user_id):

    for order in orders.values():

        if order["user_id"] == user_id:

            return order

    return None


def delete_order(order_id):

    if order_id in orders:

        del orders[order_id]
