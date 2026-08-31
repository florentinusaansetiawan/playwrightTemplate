from core.data_driven import DataDriven


DEFAULT_DATA = {

    "method": "GET",

    "path": "/booking/2",

    "headers": {
        "Content-Type": "application/json"
    },

    "expected": {
        "status_code": 200,

        "body": {
            "firstname": {
                "exists": True
            },

            "lastname": {
                "exists": True
            },

            "totalprice": {
                "exists": True
            },

            "depositpaid": {
                "exists": True
            },

            "bookingdates": {
                "exists": True
            }
        }
    }
}


def run(api, data=None):

    return DataDriven.run(
        api,
        DEFAULT_DATA,
        data
    )


def test_get_booking(api):

    result = run(api)

    assert result["status"] == "PASSED"