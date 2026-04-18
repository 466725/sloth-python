import os
import pytest
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


@pytest.fixture(scope="session")
def qtest():
    return QTestClient(
        base_url=os.getenv("QTEST_BASE_URL"),
        project_id=int(os.getenv("QTEST_PROJECT_ID")),
        token=os.getenv("QTEST_API_TOKEN"),
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # only act after test call (not setup/teardown)
    if report.when != "call":
        return

    qtest_client = item.session._qtest_client

    # get test case id from marker
    marker = item.get_closest_marker("qtest_id")
    if not marker:
        return

    test_case_id = marker.args[0]

    status = STATUS_MAP.get(report.outcome, "FAILED")
    note = str(report.longrepr) if report.failed else "Test passed"

    # create run + submit result
    test_run_id = qtest_client.create_test_run(item.name, test_case_id)
    qtest_client.submit_test_log(test_run_id, status, note)


def pytest_sessionstart(session):
    # attach client to session (simple global access)
    session._qtest_client = QTestClient(
        base_url=os.getenv("QTEST_BASE_URL"),
        project_id=int(os.getenv("QTEST_PROJECT_ID")),
        token=os.getenv("QTEST_API_TOKEN"),
    )
