import copy
import json

from core.context import TestContext
from core.test_executor import TestExecutor


class DataDriven:

    # ======================================================
    # RUN TEST
    # ======================================================

    @staticmethod
    def run(
        api,
        default_data,
        data=None
    ):
        """
        Prepare default test case data + Excel data,
        then execute the API test if execute = Y.
        """

        final_data = DataDriven.prepare(
            default_data,
            data
        )

        # ==================================================
        # EXECUTE FLAG
        # ==================================================

        execute = str(
            final_data.get(
                "execute",
                "Y"
            )
        ).strip().upper()

        if execute != "Y":

            return {
                "test_case": final_data.get(
                    "test_case",
                    ""
                ),

                "scenario": final_data.get(
                    "scenario",
                    ""
                ),

                "description": final_data.get(
                    "description",
                    ""
                ),

                "execute": execute,

                "status": "SKIPPED"
            }

        # ==================================================
        # CONTEXT
        # ==================================================

        context = TestContext()

        # ==================================================
        # EXECUTE API
        # ==================================================

        return TestExecutor.execute(

            api=api,

            context=context,

            method=final_data["method"],

            path=final_data["path"],

            # ==================================================
            # HEADERS
            # ==================================================

            default_headers=final_data.get(
                "headers"
            ),

            header_override=final_data.get(
                "header_override"
            ),

            remove_headers=final_data.get(
                "remove_headers"
            ),

            # ==================================================
            # BODY
            # ==================================================

            default_body=final_data.get(
                "body"
            ),

            body_override=final_data.get(
                "body_override"
            ),

            remove_fields=final_data.get(
                "remove_fields"
            ),

            # ==================================================
            # EXPECTED
            # ==================================================

            expected=final_data.get(
                "expected",
                {}
            ),

            # ==================================================
            # METADATA
            # ==================================================

            test_case=final_data.get(
                "test_case",
                ""
            ),

            scenario=final_data.get(
                "scenario",
                "Default"
            ),

            description=final_data.get(
                "description",
                ""
            )
        )

    # ======================================================
    # PREPARE DATA
    # ======================================================

    @staticmethod
    def prepare(
        default_data,
        data=None
    ):
        """
        Merge default test case data with
        data-driven data from Excel.
        """

        result = copy.deepcopy(
            default_data
        )

        # ==================================================
        # DEFAULT EXECUTE
        # ==================================================

        result.setdefault(
            "execute",
            "Y"
        )

        # ==================================================
        # NO DATA
        # ==================================================

        if not data:
            return result

        # ==================================================
        # EXECUTE
        # ==================================================

        if data.get("execute") is not None:

            result["execute"] = str(
                data["execute"]
            ).strip().upper()

        # ==================================================
        # BODY OVERRIDE
        # ==================================================

        if data.get("body_override"):

            result["body_override"] = (
                DataDriven._parse_json(
                    data["body_override"]
                )
            )

        # ==================================================
        # HEADER OVERRIDE
        # ==================================================

        if data.get("header_override"):

            result["header_override"] = (
                DataDriven._parse_json(
                    data["header_override"]
                )
            )

        # ==================================================
        # REMOVE FIELDS
        # ==================================================

        if data.get("remove_fields"):

            result["remove_fields"] = (
                DataDriven._parse_json(
                    data["remove_fields"]
                )
            )

        # ==================================================
        # REMOVE HEADERS
        # ==================================================

        if data.get("remove_headers"):

            result["remove_headers"] = (
                DataDriven._parse_json(
                    data["remove_headers"]
                )
            )

        # ==================================================
        # EXPECTED HTTP CODE
        # ==================================================

        if data.get("expected_http_code") is not None:

            http_code = str(
                data["expected_http_code"]
            ).strip()

            if http_code:

                try:

                    http_code = int(
                        float(http_code)
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    raise ValueError(
                        "Invalid expected_http_code: "
                        f"{data['expected_http_code']}"
                    )

                result.setdefault(
                    "expected",
                    {}
                )

                result["expected"]["http_code"] = (
                    http_code
                )

        # ==================================================
        # EXPECTED OVERRIDE
        # ==================================================

        if data.get("expected_override"):

            expected_override = (
                DataDriven._parse_json(
                    data["expected_override"]
                )
            )

            if expected_override is not None:

                result["expected"] = (
                    DataDriven._deep_merge(
                        result.get(
                            "expected",
                            {}
                        ),
                        expected_override
                    )
                )

        # ==================================================
        # METADATA
        # ==================================================

        for field in [
            "test_case",
            "scenario",
            "description"
        ]:

            if data.get(field) is not None:

                result[field] = data[field]

        return result

    # ======================================================
    # DEEP MERGE
    # ======================================================

    @staticmethod
    def _deep_merge(
        base,
        override
    ):
        """
        Deep merge override data into base data.

        Example:

        base:
        {
            "body": {
                "booking.firstname": "Jim",
                "booking.lastname": "Brown"
            }
        }

        override:
        {
            "body": {
                "booking.firstname": "Aan"
            }
        }

        Result:
        {
            "body": {
                "booking.firstname": "Aan",
                "booking.lastname": "Brown"
            }
        }
        """

        if not isinstance(
            base,
            dict
        ):

            return copy.deepcopy(
                override
            )

        result = copy.deepcopy(
            base
        )

        if not isinstance(
            override,
            dict
        ):

            return result

        for key, value in override.items():

            if (
                key in result
                and isinstance(
                    result[key],
                    dict
                )
                and isinstance(
                    value,
                    dict
                )
            ):

                result[key] = (
                    DataDriven._deep_merge(
                        result[key],
                        value
                    )
                )

            else:

                result[key] = copy.deepcopy(
                    value
                )

        return result

    # ======================================================
    # JSON PARSER
    # ======================================================

    @staticmethod
    def _parse_json(
        value
    ):

        if isinstance(
            value,
            (dict, list)
        ):

            return value

        if value is None:
            return None

        if isinstance(
            value,
            str
        ):

            value = value.strip()

            if not value:
                return None

            try:

                return json.loads(
                    value
                )

            except json.JSONDecodeError:

                raise ValueError(
                    f"Invalid JSON data: {value}"
                )

        return value