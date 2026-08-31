class TestLogger:

    # ======================================================
    # ANSI COLORS
    # ======================================================

    RESET = "\033[0m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    # ======================================================
    # TEST START
    # ======================================================

    @classmethod
    def start(
        cls,
        test_case,
        scenario,
        method,
        url
    ):

        print()
        print(
            f"{cls.CYAN}"
            f"{'=' * 70}"
            f"{cls.RESET}"
        )

        print(
            f"{cls.CYAN}"
            f"TEST CASE : "
            f"{cls.WHITE}{test_case}"
            f"{cls.RESET}"
        )

        print(
            f"{cls.CYAN}"
            f"SCENARIO  : "
            f"{cls.WHITE}{scenario}"
            f"{cls.RESET}"
        )

        print(
            f"{cls.CYAN}"
            f"REQUEST   : "
            f"{cls.WHITE}{method} {url}"
            f"{cls.RESET}"
        )

        print(
            f"{cls.CYAN}"
            f"{'=' * 70}"
            f"{cls.RESET}"
        )

    # ======================================================
    # PASSED
    # ======================================================

    @classmethod
    def passed(
        cls,
        duration
    ):

        print(
            f"{cls.GREEN}"
            f"✓ PASSED"
            f"{cls.RESET}"
            f"  ({duration} ms)"
        )

    # ======================================================
    # FAILED
    # ======================================================

    @classmethod
    def failed(
        cls,
        validation,
        duration
    ):

        print(
            f"{cls.RED}"
            f"✗ FAILED"
            f"{cls.RESET}"
            f"  ({duration} ms)"
        )

        print()

        print(
            f"{cls.RED}"
            f"ASSERTIONS"
            f"{cls.RESET}"
        )

        assertions = validation.get(
            "assertions",
            []
        )

        for assertion in assertions:

            cls._print_assertion(
                assertion
            )

    # ======================================================
    # ASSERTION
    # ======================================================

    @classmethod
    def _print_assertion(
        cls,
        assertion
    ):

        # Support beberapa kemungkinan
        # struktur assertion

        passed = assertion.get(
            "passed",
            False
        )

        message = assertion.get(
            "message",
            ""
        )

        field = assertion.get(
            "field",
            ""
        )

        expected = assertion.get(
            "expected"
        )

        actual = assertion.get(
            "actual"
        )

        if passed:

            print(
                f"  {cls.GREEN}"
                f"✓"
                f"{cls.RESET} "
                f"{message}"
            )

            return

        print(
            f"  {cls.RED}"
            f"✗"
            f"{cls.RESET} "
            f"{field or message}"
        )

        if expected is not None:

            print(
                f"      Expected : "
                f"{cls.RED}"
                f"{expected}"
                f"{cls.RESET}"
            )

        if actual is not None:

            print(
                f"      Actual   : "
                f"{cls.YELLOW}"
                f"{actual}"
                f"{cls.RESET}"
            )

        if message:

            print(
                f"      Message  : "
                f"{message}"
            )

    # ======================================================
    # ERROR
    # ======================================================

    @classmethod
    def error(
        cls,
        error
    ):

        print()

        print(
            f"{cls.RED}"
            f"{'!' * 70}"
            f"{cls.RESET}"
        )

        print(
            f"{cls.RED}"
            f"ERROR"
            f"{cls.RESET}"
        )

        print(
            f"{cls.RED}"
            f"{error}"
            f"{cls.RESET}"
        )

        print(
            f"{cls.RED}"
            f"{'!' * 70}"
            f"{cls.RESET}"
        )

    # ======================================================
    # RESPONSE
    # ======================================================

    @classmethod
    def response(
        cls,
        status_code,
        duration
    ):

        print(
            f"{cls.GRAY}"
            f"Response : "
            f"{status_code} "
            f"| {duration} ms"
            f"{cls.RESET}"
        )