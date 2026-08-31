import time

from core.body_builder import BodyBuilder
from core.header_builder import HeaderBuilder
from core.response_validator import ResponseValidator
from core.test_logger import TestLogger


class TestExecutor:

    @staticmethod
    def execute(
        api,
        context,
        method,
        path,
        expected,
        default_body=None,
        body_override=None,
        remove_fields=None,
        default_headers=None,
        header_override=None,
        remove_headers=None,
        description="",
        test_case="",
        scenario=""
    ):

        start_time = time.perf_counter()

        # ==================================================
        # VARIABLES
        # ==================================================

        variables = context.all()

        # ==================================================
        # BUILD BODY
        # ==================================================

        body = BodyBuilder.build(
            default_body=default_body,
            override=body_override,
            remove_fields=remove_fields,
            variables=variables
        )

        # ==================================================
        # BUILD HEADERS
        # ==================================================

        headers = HeaderBuilder.build(
            default_headers=default_headers,
            override=header_override,
            remove_headers=remove_headers,
            variables=variables
        )

        # ==================================================
        # LOG START
        # ==================================================

        TestLogger.start(
            test_case=test_case,
            scenario=scenario,
            method=method,
            url=path
        )

        # ==================================================
        # REQUEST
        # ==================================================

        try:

            response = api.request_api(
                method=method,
                url=path,
                headers=headers,
                body=body
            )

        except Exception as error:

            duration = round(
                (
                    time.perf_counter()
                    - start_time
                ) * 1000,
                2
            )

            TestLogger.error(
                error
            )

            return {

                "test_case": test_case,

                "scenario": scenario,

                "description": description,

                "status": "FAILED",

                "duration": duration,

                "duration_ms": duration,

                "method": method,

                "url": path,

                "request_headers": headers,

                "request_body": body,

                "request": {
                    "method": method,
                    "url": path,
                    "headers": headers,
                    "body": body
                },

                "response_status": None,

                "response_headers": {},

                "response_body": None,

                "response": {
                    "status_code": None,
                    "headers": {},
                    "body": None
                },

                "assertions": [],

                "error": str(error)
            }

        # ==================================================
        # VALIDATION
        # ==================================================

        validator = ResponseValidator()

        validation = validator.verify(
            response,
            expected
        )

        # ==================================================
        # DURATION
        # ==================================================

        duration = round(
            (
                time.perf_counter()
                - start_time
            ) * 1000,
            2
        )

        # ==================================================
        # REQUEST DATA
        # ==================================================

        request_data = response.get(
            "request",
            {}
        )

        request_method = request_data.get(
            "method",
            method
        )

        request_url = request_data.get(
            "url",
            path
        )

        request_headers = request_data.get(
            "headers",
            headers
        )

        request_body = request_data.get(
            "body",
            body
        )

        # ==================================================
        # RESPONSE DATA
        # ==================================================

        response_status = response.get(
            "status_code"
        )

        response_headers = response.get(
            "headers",
            {}
        )

        response_body = response.get(
            "body"
        )

        # ==================================================
        # LOG RESPONSE
        # ==================================================

        TestLogger.response(
            status_code=response_status,
            duration=duration
        )

        # ==================================================
        # LOG RESULT
        # ==================================================

        if validation["passed"]:

            TestLogger.passed(
                duration
            )

        else:

            TestLogger.failed(
                validation=validation,
                duration=duration
            )

        # ==================================================
        # RESULT
        # ==================================================

        result = {

            # ==============================================
            # TEST INFORMATION
            # ==============================================

            "test_case": test_case,

            "scenario": scenario,

            "description": description,

            "status": (
                "PASSED"
                if validation["passed"]
                else "FAILED"
            ),

            # ==============================================
            # TIMING
            # ==============================================

            "duration": duration,

            "duration_ms": duration,

            # ==============================================
            # REQUEST
            # ==============================================

            "method": request_method,

            "url": request_url,

            "request_headers": request_headers,

            "request_body": request_body,

            "request": request_data,

            # ==============================================
            # RESPONSE
            # ==============================================

            "response_status": response_status,

            "response_headers": response_headers,

            "response_body": response_body,

            "response": {

                "status_code": response_status,

                "headers": response_headers,

                "body": response_body
            },

            # ==============================================
            # ASSERTIONS
            # ==============================================

            "assertions": validation["assertions"]
        }

        return result