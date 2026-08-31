import pytest

from playwright.sync_api import Playwright

from core.api_client import APIClient
from utils.config import Config


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="staging",
        help="Environment: dev, staging, uat"
    )


@pytest.fixture(scope="session")
def config(request):
    environment = request.config.getoption("--env")

    return Config(environment)


@pytest.fixture
def api_context(
    playwright: Playwright,
    config
):
    context = playwright.request.new_context(
        base_url=config.base_url
    )

    yield context

    context.dispose()


@pytest.fixture
def api(api_context):
    return APIClient(api_context)