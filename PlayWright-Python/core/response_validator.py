class ResponseValidator:

    def __init__(self):
        self.results = []

    # ======================================================
    # MAIN VERIFY
    # ======================================================

    def verify(self, response, expected):
        self.results = []

        # --------------------------------------------------
        # STATUS CODE
        # --------------------------------------------------

        if "status_code" in expected:

            self._assert(
                name="status_code",
                actual=response["status_code"],
                expected=expected["status_code"],
                condition="equals"
            )

        # --------------------------------------------------
        # RESPONSE BODY
        # --------------------------------------------------

        body_expected = expected.get(
            "body",
            {}
        )

        for path, expectation in body_expected.items():

            actual = self._get_value(
                response["body"],
                path
            )

            self._validate_field(
                path,
                actual,
                expectation
            )

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        passed = all(
            result["passed"]
            for result in self.results
        )

        return {
            "passed": passed,
            "assertions": self.results
        }

    # ======================================================
    # FIELD VALIDATION
    # ======================================================

    def _validate_field(
        self,
        path,
        actual,
        expectation
    ):

        # Simple:
        #
        # "firstname": "John"
        #

        if not isinstance(
            expectation,
            dict
        ):

            self._assert(
                name=path,
                actual=actual,
                expected=expectation,
                condition="equals"
            )

            return

        # --------------------------------------------------
        # EXISTS
        # --------------------------------------------------

        if "exists" in expectation:

            exists = actual is not None

            self._assert(
                name=path,
                actual=exists,
                expected=expectation["exists"],
                condition="equals"
            )

        # --------------------------------------------------
        # EQUALS
        # --------------------------------------------------

        if "equals" in expectation:

            self._assert(
                name=path,
                actual=actual,
                expected=expectation["equals"],
                condition="equals"
            )

        # --------------------------------------------------
        # NOT EQUALS
        # --------------------------------------------------

        if "not_equals" in expectation:

            self._assert(
                name=path,
                actual=actual,
                expected=expectation["not_equals"],
                condition="not_equals"
            )

        # --------------------------------------------------
        # CONTAINS
        # --------------------------------------------------

        if "contains" in expectation:

            expected_value = expectation["contains"]

            passed = (
                actual is not None
                and expected_value in actual
            )

            self.results.append({
                "name": path,
                "condition": "contains",
                "expected": expected_value,
                "actual": actual,
                "passed": passed
            })

        # --------------------------------------------------
        # TYPE
        # --------------------------------------------------

        if "type" in expectation:

            expected_type = expectation["type"]

            type_map = {
                "string": str,
                "integer": int,
                "number": (int, float),
                "boolean": bool,
                "object": dict,
                "array": list
            }

            python_type = type_map.get(
                expected_type
            )

            passed = (
                python_type is not None
                and isinstance(
                    actual,
                    python_type
                )
            )

            self.results.append({
                "name": path,
                "condition": "type",
                "expected": expected_type,
                "actual": (
                    type(actual).__name__
                    if actual is not None
                    else None
                ),
                "passed": passed
            })

    # ======================================================
    # ASSERT
    # ======================================================

    def _assert(
        self,
        name,
        actual,
        expected,
        condition
    ):

        if condition == "equals":

            passed = actual == expected

        elif condition == "not_equals":

            passed = actual != expected

        else:

            passed = False

        self.results.append({
            "name": name,
            "condition": condition,
            "expected": expected,
            "actual": actual,
            "passed": passed
        })

    # ======================================================
    # GET NESTED VALUE
    # ======================================================

    @staticmethod
    def _get_value(data, path):

        if data is None:
            return None

        current = data

        for key in path.split("."):

            if isinstance(current, dict):

                if key not in current:
                    return None

                current = current[key]

            elif isinstance(current, list):

                try:
                    current = current[
                        int(key)
                    ]

                except (
                    ValueError,
                    IndexError
                ):
                    return None

            else:
                return None

        return current