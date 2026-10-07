"""Shared fixtures for the DSA API suites.

Each test runs against an in-process FastAPI application wired to a throwaway
``.env`` file and SQLite database, so suites never touch the developer's real
configuration, never require live credentials, and stay independent of each
other's data.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

# litellm is an optional heavyweight dependency; stub it so importing the API
# package never pulls the real client into the test process.
if "litellm" not in sys.modules:
    try:  # pragma: no cover - depends on the local environment
        import litellm  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover - exercised on slim installs
        sys.modules["litellm"] = MagicMock()

import ai_stock.auth as auth
from ai_stock.config import Config
from ai_stock.core import market_review_lock
from ai_stock.storage import DatabaseManager
from api.app import create_app

REPO_ROOT = Path(__file__).resolve().parents[3]
API_SPEC_PATH = REPO_ROOT / "docs" / "api_spec.json"
REPO_ENV_PATH = REPO_ROOT / ".env"

#: Minimal offline configuration. No provider credentials are supplied so that
#: optional integrations stay disabled unless a test explicitly enables them,
#: and the remote stock index refresh is switched off to keep runs network-free.
BASE_ENV = {
    "ADMIN_AUTH_ENABLED": "false",
    "AGENT_MODE": "false",
    "STOCK_LIST": "600519,000858",
    "ENABLE_NOTIFICATION": "false",
    "REPORT_LANGUAGE": "zh",
    "STOCK_INDEX_REMOTE_UPDATE_ENABLED": "false",
}


@dataclass
class ApiEnvironment:
    """Filesystem locations backing one isolated API test environment."""

    root: Path
    env_file: Path
    database: Path
    static_dir: Path

    def read_env(self) -> dict[str, str]:
        """Return the current ``.env`` contents as a key/value mapping."""
        values: dict[str, str] = {}
        for line in self.env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
        return values


def _reset_runtime_state() -> None:
    """Drop cached singletons so each test observes a clean runtime."""
    auth._auth_enabled = None
    auth._session_secret = None
    auth._password_hash_salt = None
    auth._password_hash_stored = None
    auth._rate_limit = {}
    market_review_lock._market_review_running = False
    Config.reset_instance()
    DatabaseManager.reset_instance()


def _strip_developer_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unset any variable the developer's own ``.env`` injected into the process.

    Importing the application loads the repository ``.env`` into ``os.environ``
    before any fixture runs, which would otherwise let local credentials reach
    the suites and make outbound calls possible. ``monkeypatch`` restores the
    original values once the test finishes.
    """
    if not REPO_ENV_PATH.exists():
        return

    for line in REPO_ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        monkeypatch.delenv(line.partition("=")[0].strip(), raising=False)


@pytest.fixture(scope="session")
def api_spec() -> dict[str, Any]:
    """Load the published OpenAPI contract used for spec-driven assertions."""
    return json.loads(API_SPEC_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def api_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[ApiEnvironment]:
    """Create an isolated ``.env`` + SQLite environment for a single test."""
    env_file = tmp_path / ".env"
    database = tmp_path / "api_suite.db"
    static_dir = tmp_path / "static"
    static_dir.mkdir()

    settings = {**BASE_ENV, "DATABASE_PATH": str(database)}
    env_file.write_text(
        "\n".join(f"{key}={value}" for key, value in settings.items()) + "\n",
        encoding="utf-8",
    )

    _strip_developer_env(monkeypatch)
    monkeypatch.setenv("ENV_FILE", str(env_file))
    monkeypatch.setenv("DATABASE_PATH", str(database))
    monkeypatch.setenv("AGENT_MODE", "false")
    monkeypatch.setenv("STOCK_INDEX_REMOTE_UPDATE_ENABLED", "false")
    monkeypatch.delenv("DSA_DESKTOP_MODE", raising=False)
    monkeypatch.delenv("CORS_ALLOW_ALL", raising=False)

    _reset_runtime_state()
    try:
        yield ApiEnvironment(
            root=tmp_path,
            env_file=env_file,
            database=database,
            static_dir=static_dir,
        )
    finally:
        _reset_runtime_state()


@pytest.fixture
def api_client(api_env: ApiEnvironment) -> TestClient:
    """Provide an API client with admin authentication disabled.

    The client is intentionally created without entering its context manager so
    the application lifespan, which schedules a remote stock-index refresh, does
    not run during tests.
    """
    return TestClient(create_app(static_dir=api_env.static_dir))


@pytest.fixture
def auth_enabled_client(api_env: ApiEnvironment, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Provide an unauthenticated client against an auth-protected application."""
    monkeypatch.setattr("api.middlewares.auth.is_auth_enabled", lambda: True)
    return TestClient(create_app(static_dir=api_env.static_dir))


@pytest.fixture
def db_manager(api_client: TestClient) -> DatabaseManager:
    """Return the database manager backing the active API client."""
    return DatabaseManager.get_instance()
