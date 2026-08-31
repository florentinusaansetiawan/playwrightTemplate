import copy
import re


class HeaderBuilder:

    @staticmethod
    def build(
        default_headers=None,
        override=None,
        remove_headers=None,
        variables=None
    ):
        headers = copy.deepcopy(
            default_headers
        ) if default_headers else {}

        # ==================================================
        # OVERRIDE
        # ==================================================

        if override:
            headers.update(
                copy.deepcopy(override)
            )

        # ==================================================
        # REMOVE HEADERS
        # ==================================================

        if remove_headers:
            for header in remove_headers:
                headers.pop(header, None)

        # ==================================================
        # VARIABLE REPLACEMENT
        # ==================================================

        if variables:
            headers = HeaderBuilder._replace_variables(
                headers,
                variables
            )

        return headers

    # ======================================================
    # VARIABLE REPLACEMENT
    # ======================================================

    @staticmethod
    def _replace_variables(data, variables):

        if isinstance(data, dict):

            return {
                key: HeaderBuilder._replace_variables(
                    value,
                    variables
                )
                for key, value in data.items()
            }

        if isinstance(data, list):

            return [
                HeaderBuilder._replace_variables(
                    value,
                    variables
                )
                for value in data
            ]

        if isinstance(data, str):

            pattern = r"\$\{([^}]+)\}"

            def replace(match):

                variable = match.group(1)

                if variable in variables:
                    return str(
                        variables[variable]
                    )

                return match.group(0)

            return re.sub(
                pattern,
                replace,
                data
            )

        return data