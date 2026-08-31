from core.data_driven import DataDriven


# ======================================================
# DEFAULT DATA
# ======================================================

DEFAULT_DATA = {

    "method": "POST",

    "path": "/booking",

    "headers": {
        "Content-Type": "application/json",
        "User-Agent": "aanqa-python-requests/2.31.0"
    },

    "body": {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,

        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },

        "additionalneeds": "Breakfast"
    },

    "expected": {

        "status_code": 200,

        "headers": {
            "Content-Type": "application/json"
        },

        "body": {

            "bookingid": {
                "exists": True,
                "type": "integer"
            },

            "booking.firstname": "Jim",

            "booking.lastname": "Brown",

            "booking.totalprice": 111,

            "booking.depositpaid": True
        }
    }
}


# ======================================================
# RUN
# ======================================================

def run(
    api,
    data=None
):

    return DataDriven.run(
        api=api,
        default_data=DEFAULT_DATA,
        data=data
    )


# ======================================================
# PYTEST
# ======================================================

def test_create_booking(api):

    result = run(api)

    assert result["status"] == "PASSED"