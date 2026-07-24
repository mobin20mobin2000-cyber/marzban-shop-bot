# =========================
# plans.py
# Zeus Shop VPN
# =========================


PLANS = {


    "10GB": {

        "name": "۱۰ گیگ",

        "volume": 10 * 1024 * 1024 * 1024,

        "days": 30,

        "price": 10000

    },


    "20GB": {

        "name": "۲۰ گیگ",

        "volume": 20 * 1024 * 1024 * 1024,

        "days": 30,

        "price": 20000

    },


    "50GB": {

        "name": "۵۰ گیگ",

        "volume": 50 * 1024 * 1024 * 1024,

        "days": 30,

        "price": 50000

    },


    "100GB": {

        "name": "۱۰۰ گیگ",

        "volume": 100 * 1024 * 1024 * 1024,

        "days": 30,

        "price": 100000

    }

}




def get_plan(plan_id):

    return PLANS.get(
        plan_id
    )
