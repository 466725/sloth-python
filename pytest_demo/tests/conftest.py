import os
import sqlite3

import pytest

from utils.data_base import connect_mysql, connection_scope
from utils.qtest_client import QTestClient

STATUS_MAP = {
    "passed": "PASSED",
    "failed": "FAILED",
    "skipped": "BLOCKED",
}

QTEST_CONFIG_VARS = (
    "QTEST_BASE_URL",
    "QTEST_PROJECT_ID",
    "QTEST_API_TOKEN",
)


def _build_qtest_client():
    base_url, project_id, token = (os.getenv(name) for name in QTEST_CONFIG_VARS)

    if not all((base_url, project_id, token)):
        return None

    return QTestClient(
        base_url=base_url,
        project_id=int(project_id),
        token=token,
    )


def _build_connection_factory():
    backend = os.getenv("SLOTH_PYTEST_DB_BACKEND", "sqlite").strip().lower()

    if backend == "sqlite":
        sqlite_path = os.getenv("SLOTH_PYTEST_SQLITE_PATH", ":memory:")
        return lambda: sqlite3.connect(sqlite_path)

    if backend == "mysql":
        return connect_mysql

    raise ValueError("SLOTH_PYTEST_DB_BACKEND must be either 'sqlite' or 'mysql'.")


@pytest.fixture(scope="session")
def qtest():
    client = _build_qtest_client()
    if client is None:
        pytest.skip("qTest is not configured. Set QTEST_BASE_URL, QTEST_PROJECT_ID, and QTEST_API_TOKEN.")

    return client


@pytest.fixture
def db_conn():
    """Provide a managed database connection for tests.

    Defaults to an in-memory SQLite database so unit tests run without external
    services. Set SLOTH_PYTEST_DB_BACKEND=mysql to use the MySQL settings from
    utils.data_base.DatabaseConfig.from_env().
    """

    try:
        connection_factory = _build_connection_factory()
    except ValueError as error:
        pytest.fail(str(error))

    with connection_scope(connection_factory) as connection:
        try:
            yield connection
        finally:
            if hasattr(connection, "rollback"):
                connection.rollback()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # only act after test call (not setup/teardown)
    if report.when != "call":
        return

    # get test case id from marker
    marker = item.get_closest_marker("qtest_id")
    if not marker:
        return

    qtest_client = getattr(item.session, "_qtest_client", None)
    if qtest_client is None:
        return

    test_case_id = marker.args[0]

    status = STATUS_MAP.get(report.outcome, "FAILED")
    note = str(report.longrepr) if report.failed else "Test passed"

    # create run + submit result
    test_run_id = qtest_client.create_test_run(item.name, test_case_id)
    qtest_client.submit_test_log(test_run_id, status, note)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Test environment to use (default: local).",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "qtest_id(test_case_id): associate a test with a qTest test case",
    )
    config.test_environment = config.getoption("--env")


def pytest_sessionstart(session):
    # attach client to session (simple global access)
    session._qtest_client = _build_qtest_client()


def pytest_sessionfinish(session, exitstatus):
    session._qtest_client = None
