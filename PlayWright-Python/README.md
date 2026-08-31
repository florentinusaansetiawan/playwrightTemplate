# Playwright-Python API Test Framework

[English](README.md) | [Bahasa Indonesia](README.id.md)

This project is a lightweight API test framework built with Python, pytest, and Playwright's API request client. It is designed for environment-based configuration, reusable API test cases, Excel-driven scenarios, and HTML reporting for smoke validation.

## Overview

The framework supports:

- Environment switching via `--env`
- Shared `api` fixture with a Playwright request context
- Reusable test case modules under `test_case/`
- Data-driven execution from an Excel file
- Response validation using expected status and body checks
- HTML suite reports stored under `reports/`

## Requirements

- Python 3.13 or a compatible Python 3 version
- Internet access to the configured API
- PowerShell on Windows, or a similar shell

## Project Structure

```text
config/                 Environment YAML files
core/                   Shared framework logic
  api_client.py         Playwright API wrapper
  body_builder.py       Request body creation helpers
  context.py            Context helpers
  data_driven.py        Data merging + validation executor
  header_builder.py     Request header helpers
  report_manager.py     Results and HTML report generator
  report_helper.py      HTML template builder
  response_validator.py Response assertion logic
  suite_helper.py       Excel-driven suite runner
  test_executor.py      Reusable execution flow
  test_loader.py        Test loading helpers
  test_logger.py        Logging helpers

data/                   Excel test scenario files
  test_excel_contoh.xlsx
reports/                Generated HTML reports
  YYYY-MM-DD/
    test_smoke/
      test_smoke_<timestamp>.html
test_case/              Reusable API test modules
  booking/
    test_create_booking.py
    test_get_booking.py
test_suite/             Suite entry points
  smoke/
    suite_smoke.py
utils/                  Shared utilities
  config.py             YAML environment loader
  excel_utils.py        Excel reader
conftest.py             Pytest fixture and CLI option
requirements.txt        Dependency list
README.md               English documentation
README.id.md            Indonesian documentation
```

## Environment Configuration

The framework loads configuration from `config/<environment>.yaml`.

Current files:

- `config/staging.yaml` with the default Restful Booker URL
- `config/dev.yaml`
- `config/uat.yaml`

Example content:

```yaml
base_url: https://restful-booker.herokuapp.com
```

The default environment is `staging` and is set in `conftest.py`:

```python
parser.addoption(
    "--env",
    action="store",
    default="staging",
    help="Environment: dev, staging, uat"
)
```

To run a suite against a specific environment:

```powershell
pytest -v --env dev .\test_suite\smoke\suite_smoke.py
pytest -v --env staging .\test_suite\smoke\suite_smoke.py
pytest -v --env uat .\test_suite\smoke\suite_smoke.py
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If browser-based tests are added later, install Playwright browsers:

```powershell
playwright install
```

## How the Framework Works

1. `conftest.py` reads the `--env` flag and loads the matching YAML config via `utils/config.py`.
2. The `api` fixture creates a Playwright request context with `base_url` from the environment config.
3. A test module exposes a `run(api, data=None)` function and returns the result from `DataDriven.run(...)`.
4. `SuiteHelper.run(...)` reads the Excel sheet, filters rows with `execute = Y`, imports the matching test module, and executes it.
5. `ReportManager.generate()` writes the HTML result under `reports/YYYY-MM-DD/<suite_name>/`.

## Running Tests

Run a single booking test directly:

```powershell
pytest -v .\test_case\booking\test_create_booking.py
pytest -v .\test_case\booking\test_get_booking.py
```

Run the smoke suite:

```powershell
pytest -v .\test_suite\smoke\suite_smoke.py
```

Run all tests in the project:

```powershell
pytest -v
```

Run a specific test by keyword:

```powershell
pytest -v .\test_case\booking\test_create_booking.py -k test_create_booking
```

Show what pytest will collect without running it:

```powershell
pytest --collect-only -q
```

## Smoke Suite and Excel Data

The smoke suite loads data from `data/test_excel_contoh.xlsx` and reads the `API_TEST` sheet.

Each row is treated as a scenario with fields such as:

- `execute`
- `test_case`
- additional request overrides and expected result values

The suite helper imports modules using `test_case.<test_case>` pattern, for example:

```python
module = importlib.import_module(f"test_case.{test_case}")
result = module.run(api, data)
```

## Reports

When the smoke suite runs, it creates an HTML file in the following structure:

```text
reports/2026-08-31/test_smoke/test_smoke_20260831_082812.html
```

The generated report contains the suite summary, individual test result status, request details, response details, and execution timing.

## Adding a New Test Case

1. Create or update a module under `test_case/`.
2. Expose a `run(api, data=None)` function.
3. Put the default request and expected values in the module.
4. Add or update the scenario row in `data/test_excel_contoh.xlsx`.
5. Run the specific test and then run the smoke suite.

Example pattern:

```python
def run(api, data=None):
    return DataDriven.run(api=api, default_data=DEFAULT_DATA, data=data)
```

## Troubleshooting

- If pytest raises a config error, confirm `config/<environment>.yaml` exists and includes `base_url`.
- If the Excel-driven suite fails to load, confirm `data/test_excel_contoh.xlsx` exists and includes the `API_TEST` worksheet.
- If an API call fails, verify the selected environment, internet access, and the configured base URL.
- If a test case cannot be imported, verify the `test_case` value in the Excel file matches the module path without the `.py` extension.

## Notes

This repository currently uses the Restful Booker API as the target service for smoke validation and booking scenarios.
