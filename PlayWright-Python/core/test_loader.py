import importlib


class TestLoader:

    @staticmethod
    def load(test_case):

        if not test_case:
            raise ValueError(
                "test_case is required"
            )

        test_case = test_case.strip()

        parts = test_case.split(".")

        if len(parts) < 2:
            raise ValueError(
                f"Invalid test_case: {test_case}"
            )

        # ==============================================
        # MODULE
        # ==============================================

        module_name = (
            "test_case."
            + ".".join(parts)
        )

        # ==============================================
        # FUNCTION
        # ==============================================

        function_name = parts[-1]

        # ==============================================
        # IMPORT
        # ==============================================

        try:

            module = importlib.import_module(
                module_name
            )

        except ImportError as e:

            raise ImportError(
                f"Cannot load test case: "
                f"{test_case}\n"
                f"Module: {module_name}\n"
                f"Error: {e}"
            ) from e

        # ==============================================
        # GET FUNCTION
        # ==============================================

        try:

            return getattr(
                module,
                function_name
            )

        except AttributeError as e:

            raise AttributeError(
                f"Test function "
                f"'{function_name}' "
                f"not found in "
                f"'{module_name}'"
            ) from e