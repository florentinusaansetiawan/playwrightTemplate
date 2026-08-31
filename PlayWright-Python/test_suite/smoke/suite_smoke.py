from core.suite_helper import SuiteHelper


EXCEL_FILE = "data/test_excel_contoh.xlsx"

SHEET_NAME = "API_TEST"

SUITE_NAME = "test_smoke"


def test_smoke(api):

    SuiteHelper.run(
        api=api,
        excel_file=EXCEL_FILE,
        sheet_name=SHEET_NAME,
        suite_name=SUITE_NAME
    )