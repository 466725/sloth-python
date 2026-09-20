"""Pytest hooks and their relationship to TestNG lifecycle annotations.

Pytest hooks are framework extension points named according to pytest's hook
specification, such as ``pytest_sessionstart`` and ``pytest_sessionfinish``.
They customize pytest itself: configuration, collection, execution, and
reporting. Pytest fixtures are usually the closer equivalent to TestNG's
``@BeforeClass``, ``@AfterClass``, ``@BeforeMethod``, and ``@AfterMethod``
annotations because fixtures manage setup and teardown around test resources.
"""

# See -> pytest_tests/conftest.py
