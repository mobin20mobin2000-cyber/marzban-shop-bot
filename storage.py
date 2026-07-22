import json
import os


USERS_FILE = "users.json"

ORDERS_FILE = "orders.json"





# =========================
# کاربران
# =========================

def load_users():

    if not os.path.exists(USERS_FILE):

        return {}


    with open(
        USERS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)





def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            users,
            f,
            ensure_ascii=False,
            indent=4
        )





def save_service(
    user_id,
    username,
    subscription
):

    users = load_users()


    users[str(user_id)] = {

        "username": username,

        "subscription": subscription

    }


    save_users(users)





def get_service(user_id):

    users = load_users()


    return users.get(
        str(user_id)
    )





# =========================
# سفارش ها
# =========================

def load_orders():

    if not os.path.exists(ORDERS_FILE):

        return {}


    with open(
        ORDERS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)





def save_orders(orders):

    with open(
        ORDERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            orders,
            f,
            ensure_ascii=False,
            indent=4
        )





def save_order(
    order_id,
    user_id,
    plan
):

    orders = load_orders()


    orders[str(order_id)] = {

        "order_id": order_id,

        "user_id": user_id,

        "plan": plan

    }


    save_orders(orders)





def get_order(value):

    orders = load_orders()


    # پیدا کردن با شماره سفارش

    if str(value) in orders:

        return orders[str(value)]



    # پیدا کردن با آیدی کاربر

    for order in orders.values():

        if order["user_id"] == value:

            return order



    return None





def delete_order(order_id):

    orders = load_orders()


    if str(order_id) in orders:

        del orders[str(order_id)]


    save_orders(orders)
