PLANS = {

    "10GB": {
        "name": "۱۰ گیگ",
        "volume": 10,
        "price": "50000"
    },


    "20GB": {
        "name": "۲۰ گیگ",
        "volume": 20,
        "price": "100000"
    },


    "50GB": {
        "name": "۵۰ گیگ",
        "volume": 50,
        "price": "250000"
    },


    "100GB": {
        "name": "۱۰۰ گیگ",
        "volume": 100,
        "price": "500000"
    }

}


def get_plan(plan_id):

    return PLANS.get(plan_id)
