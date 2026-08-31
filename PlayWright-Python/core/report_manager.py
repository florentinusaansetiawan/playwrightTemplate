from datetime import datetime
from pathlib import Path

from core.report_helper import ReportHelper


class ReportManager:

    _results = []
    _suite_name = None
    _start_time = None

    # ======================================================
    # START SUITE
    # ======================================================

    @classmethod
    def start_suite(
        cls,
        suite_name
    ):

        cls._results = []

        cls._suite_name = (
            suite_name
            or "test_suite"
        )

        cls._start_time = datetime.now()

    # ======================================================
    # ADD RESULT
    # ======================================================

    @classmethod
    def add_result(
        cls,
        result
    ):

        cls._results.append(
            result
        )

    # ======================================================
    # GENERATE REPORT
    # ======================================================

    @classmethod
    def generate(cls):

        if not cls._suite_name:

            cls._suite_name = (
                "test_suite"
            )

        if cls._start_time is None:

            cls._start_time = (
                datetime.now()
            )

        end_time = datetime.now()

        duration = (
            end_time
            - cls._start_time
        ).total_seconds()

        # ==================================================
        # DATE
        # ==================================================

        report_date = end_time.strftime(
            "%Y-%m-%d"
        )

        timestamp = end_time.strftime(
            "%Y%m%d_%H%M%S"
        )

        # ==================================================
        # REPORT DIRECTORY
        #
        # reports/
        #   YYYY-MM-DD/
        #       suite_name/
        #           report.html
        # ==================================================

        report_dir = (
            Path("reports")
            / report_date
            / cls._suite_name
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # REPORT FILE
        # ==================================================

        report_file = (
            report_dir
            / (
                f"{cls._suite_name}_"
                f"{timestamp}.html"
            )
        )

        # ==================================================
        # SUMMARY
        # ==================================================

        total = len(
            cls._results
        )

        passed = sum(

            1

            for result in cls._results

            if result.get(
                "status"
            ) == "PASSED"

        )

        failed = sum(

            1

            for result in cls._results

            if result.get(
                "status"
            ) == "FAILED"

        )

        # ==================================================
        # BUILD HTML
        # ==================================================

        html_content = (
            ReportHelper.build_html(

                suite_name=cls._suite_name,

                results=cls._results,

                total=total,

                passed=passed,

                failed=failed,

                duration=duration

            )
        )

        # ==================================================
        # WRITE
        # ==================================================

        report_file.write_text(
            html_content,
            encoding="utf-8"
        )

        return report_file
