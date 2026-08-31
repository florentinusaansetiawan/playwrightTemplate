import copy
import re


class BodyBuilder:

    @staticmethod
    def build(
        default_body=None,
        override=None,
        remove_fields=None,
        variables=None
    ):
        body = copy.deepcopy(default_body) if default_body else {}

        # ==================================================
        # OVERRIDE
        # ==================================================

        if override:
            BodyBuilder._merge(body, override)

        # ==================================================
        # REMOVE FIELDS
        # ==================================================

        if remove_fields:
            for field in remove_fields:
                BodyBuilder._remove(body, field)

        # ==================================================
        # VARIABLE REPLACEMENT
        # ==================================================

        if variables:
            body = BodyBuilder._replace_variables(
                body,
                variables
            )

        return body

    # ======================================================
    # MERGE
    # ======================================================

    @staticmethod
    def _merge(target, source):

        for key, value in source.items():

            if (
                key in target
                and isinstance(target[key], dict)
                and isinstance(value, dict)
            ):
                BodyBuilder._merge(
                    target[key],
                    value
                )
            else:
                target[key] = copy.deepcopy(value)

    # ======================================================
    # REMOVE
    # ======================================================

    @staticmethod
    def _remove(data, path):

        parts = path.split(".")

        current = data

        for part in parts[:-1]:

            if not isinstance(current, dict):
                return

            if part not in current:
                return

            current = current[part]

        if isinstance(current, dict):
            current.pop(parts[-1], None)

    # ======================================================
    # VARIABLE REPLACEMENT
    # ======================================================

    @staticmethod
    def _replace_variables(data, variables):

        if isinstance(data, dict):

            return {
                key: BodyBuilder._replace_variables(
                    value,
                    variables
                )
                for key, value in data.items()
            }

        if isinstance(data, list):

            return [
                BodyBuilder._replace_variables(
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