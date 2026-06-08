import os
import sqlite3

import pytest

from utils.data_base import connect_mysql, connection_scope
from utils.qtest_client import QTestClient

# map pytest outcome → qTest status
STATUS_MAP = {
    "passed": "PASSED",
    "failed": "FAILED",
    "skipped": "BLOCKED"
}

"""
Setup below values as system environment variables:
QTEST_BASE_URL=https://yourcompany.qtestnet.com
QTEST_PROJECT_ID=123456
QTEST_API_TOKEN=your_token_here
"""


def _build_qtest_client():
    base_url = os.getenv("QTEST_BASE_URL")
    project_id = os.getenv("QTEST_PROJECT_ID")
    token = os.getenv("QTEST_API_TOKEN")

    if not all([base_url, project_id, token]):
        return None

    return QTestClient(
        base_url=base_url,
        project_id=int(project_id),
        token=token,
    )


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

    backend = os.getenv("SLOTH_PYTEST_DB_BACKEND", "sqlite").strip().lower()

    if backend == "sqlite":
        sqlite_path = os.getenv("SLOTH_PYTEST_SQLITE_PATH", ":memory:")
        connection_factory = lambda: sqlite3.connect(sqlite_path)
    elif backend == "mysql":
        connection_factory = connect_mysql
    else:
        pytest.fail("SLOTH_PYTEST_DB_BACKEND must be either 'sqlite' or 'mysql'.")

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


def pytest_sessionstart(session):
    # attach client to session (simple global access)
    session._qtest_client = _build_qtest_client()
