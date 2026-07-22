import time


orders = {}


def create_order(user_id, plan):

    order_id = str(
        int(time.time())
    )

    orders[order_id] = {
        "user_id": user_id,
        "plan": plan,
        "status": "waiting"
    }

    return order_id



def get_order(order_id):

    return orders.get(
        order_id
    )



def approve_order(order_id):

    if order_id in orders:

        orders[order_id]["status"] = "approved"

        return True

    return False



def reject_order(order_id):

    if order_id in orders:

        orders[order_id]["status"] = "rejected"

        return True

    return False



def user_orders(user_id):

    result = []

    for order_id, data in orders.items():

        if data["user_id"] == user_id:

            result.append(
                {
                    "id": order_id,
                    **data
                }
            )

    return result
