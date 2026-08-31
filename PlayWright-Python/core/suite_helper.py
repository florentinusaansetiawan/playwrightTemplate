import importlib
from pathlib import Path

from core.report_manager import ReportManager
from utils.excel_utils import ExcelUtils


class SuiteHelper:

    @staticmethod
    def run(
        api,
        excel_file,
        sheet_name,
        suite_name
    ):

        # ==================================================
        # PROJECT ROOT
        # ==================================================

        project_root = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        excel_path = (
            project_root
            / excel_file
        )

        # ==================================================
        # VALIDATE EXCEL
        # ==================================================

        if not excel_path.exists():

            raise FileNotFoundError(
                f"Excel file not found:\n"
                f"{excel_path}"
            )

        # ==================================================
        # START REPORT
        # ==================================================

        ReportManager.start_suite(
            suite_name
        )

        # ==================================================
        # READ EXCEL
        # ==================================================

        test_data = ExcelUtils.read(
            str(excel_path),
            sheet_name
        )

        # ==================================================
        # EXECUTE DATA-DRIVEN TEST
        # ==================================================

        for data in test_data:

            execute = str(
                data.get(
                    "execute",
                    "Y"
                )
            ).strip().upper()

            if execute != "Y":
                continue

            test_case = data.get(
                "test_case"
            )

            if not test_case:
                continue

            # ----------------------------------------------
            # LOAD TEST CASE
            # ----------------------------------------------

            module = importlib.import_module(
                f"test_case.{test_case}"
            )

            # ----------------------------------------------
            # EXECUTE
            # ----------------------------------------------

            result = module.run(
                api,
                data
            )

            # ----------------------------------------------
            # ADD REPORT
            # ----------------------------------------------

            ReportManager.add_result(
                result
            )

        # ==================================================
        # GENERATE REPORT
        # ==================================================

        return ReportManager.generate()