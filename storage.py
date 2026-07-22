import json
import os


FILE = "users.json"



def load_users():

    if not os.path.exists(FILE):

        return {}


    with open(
        FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_users(users):

    with open(
        FILE,
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
