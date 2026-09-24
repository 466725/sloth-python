import os
import sqlite3
from uuid import uuid4

import pytest

from utils.data_base import (
    DatabaseConfig,
    connect_mysql,
    connection_scope,
    cursor_scope,
    execute_sql,
    fetch_all,
    fetch_one,
    fetch_value,
    transactional,
    with_connection,
)
from utils.data_base.sql_queries import GET_ACTIVE_USER_BY_NAME


def _mysql_env_ready() -> bool:
    return all(
        os.getenv(f"SLOTH_MYSQL_{name}") is not None
        for name in ("HOST", "PORT", "DB", "USER", "PASSWORD")
    )


def _create_users_table(connection: sqlite3.Connection) -> None:
    execute_sql(
        connection,
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )
        """,
    )


@pytest.fixture
def sqlite_users_connection():
    connection = sqlite3.connect(":memory:")
    _create_users_table(connection)
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def mysql_connection():
    if not _mysql_env_ready():
        pytest.skip("MySQL local database env vars are not configured.")

    try:
        connection = connect_mysql(DatabaseConfig.from_env())
    except Exception as exc:  # pragma: no cover - depends on local environment
        pytest.skip(f"Local MySQL database is not available: {exc}")

    try:
        yield connection
    finally:
        connection.close()


@pytest.mark.unit
def test_database_config_loads_from_environment(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SLOTH_MYSQL_HOST", "db.example.test")
    monkeypatch.setenv("SLOTH_MYSQL_PORT", "3307")
    monkeypatch.setenv("SLOTH_MYSQL_DB", "demo")
    monkeypatch.setenv("SLOTH_MYSQL_USER", "demo_user")
    monkeypatch.setenv("SLOTH_MYSQL_PASSWORD", "secret")

    config = DatabaseConfig.from_env()

    assert config.host == "db.example.test"
    assert config.port == 3307
    assert config.database == "demo"
    assert config.user == "demo_user"
    assert config.password == "secret"
    assert config.as_mysql_kwargs()["database"] == "demo"


@pytest.mark.unit
def test_build_connection_factory_defaults_to_mysql_when_mysql_env_is_configured(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SLOTH_PYTEST_DB_BACKEND", raising=False)
    monkeypatch.setenv("SLOTH_MYSQL_HOST", "db.example.test")
    monkeypatch.setenv("SLOTH_MYSQL_PORT", "3307")
    monkeypatch.setenv("SLOTH_MYSQL_DB", "demo")
    monkeypatch.setenv("SLOTH_MYSQL_USER", "demo_user")
    monkeypatch.setenv("SLOTH_MYSQL_PASSWORD", "secret")

    import pytest_tests.conftest as conftest

    assert conftest._build_connection_factory() is conftest.connect_mysql


@pytest.mark.unit
def test_local_mysql_connection_works_when_configured(mysql_connection):
    assert fetch_value(mysql_connection, "SELECT DATABASE()") == os.getenv("SLOTH_MYSQL_DB")
    assert fetch_value(mysql_connection, "SELECT 1") == 1


@pytest.mark.unit
def test_local_mysql_can_create_table_and_insert_records_when_configured(mysql_connection):
    table_name = f"test_database_client_{uuid4().hex}"

    try:
        execute_sql(
            mysql_connection,
            f"""
            CREATE TABLE `{table_name}` (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                active BOOLEAN NOT NULL
            )
            """,
        )
        rowcount = execute_sql(
            mysql_connection,
            f"INSERT INTO `{table_name}` (name, active) VALUES (%s, %s)",
            [("Ada", True), ("Grace", False)],
            many=True,
            commit=True,
        )

        assert rowcount == 2
        assert fetch_all(mysql_connection, f"SELECT name, active FROM `{table_name}` ORDER BY id") == [
            ("Ada", 1),
            ("Grace", 0),
        ]
        assert fetch_one(
            mysql_connection,
            GET_ACTIVE_USER_BY_NAME.format(table_name=table_name),
            ("Ada",),
        ) == ("Ada", 1)
    finally:
        execute_sql(mysql_connection, f"DROP TABLE IF EXISTS `{table_name}`")


@pytest.mark.unit
def test_execute_sql_supports_parameters_and_fetch_helpers(sqlite_users_connection):
    execute_sql(sqlite_users_connection, "INSERT INTO users (name, active) VALUES (?, ?)", ("Ada", 1))
    execute_sql(sqlite_users_connection, "INSERT INTO users (name, active) VALUES (?, ?)", ("Grace", 0))

    assert fetch_value(sqlite_users_connection, "SELECT COUNT(*) FROM users") == 2
    assert fetch_one(sqlite_users_connection, "SELECT name FROM users WHERE active = ?", (1,)) == ("Ada",)
    assert fetch_all(sqlite_users_connection, "SELECT name FROM users ORDER BY name") == [
        ("Ada",),
        ("Grace",),
    ]


@pytest.mark.unit
def test_execute_sql_supports_many_parameter_sets(sqlite_users_connection):
    rowcount = execute_sql(
        sqlite_users_connection,
        "INSERT INTO users (name, active) VALUES (?, ?)",
        [("Ada", 1), ("Grace", 0), ("Katherine", 1)],
        many=True,
    )

    assert rowcount == 3
    assert fetch_value(sqlite_users_connection, "SELECT COUNT(*) FROM users WHERE active = ?", (1,)) == 2


@pytest.mark.unit
def test_cursor_scope_allows_direct_cursor_usage(sqlite_users_connection):
    execute_sql(sqlite_users_connection, "INSERT INTO users (name) VALUES (?)", ("Ada",))

    with cursor_scope(sqlite_users_connection) as cursor:
        cursor.execute("SELECT name FROM users")
        row = cursor.fetchone()

    assert row == ("Ada",)


@pytest.mark.unit
def test_connection_scope_commits_and_closes_connection(tmp_path):
    db_path = tmp_path / "demo.sqlite"

    with connection_scope(lambda: sqlite3.connect(db_path), commit=True) as connection:
        _create_users_table(connection)
        execute_sql(connection, "INSERT INTO users (name) VALUES (?)", ("Ada",))

    with sqlite3.connect(db_path) as connection:
        assert fetch_value(connection, "SELECT COUNT(*) FROM users") == 1


@pytest.mark.unit
def test_connection_scope_rolls_back_on_error(tmp_path):
    db_path = tmp_path / "demo.sqlite"
    with sqlite3.connect(db_path) as connection:
        _create_users_table(connection)

    with pytest.raises(RuntimeError, match="boom"):
        with connection_scope(lambda: sqlite3.connect(db_path), commit=True) as connection:
            execute_sql(connection, "INSERT INTO users (name) VALUES (?)", ("Ada",))
            raise RuntimeError("boom")

    with sqlite3.connect(db_path) as connection:
        assert fetch_value(connection, "SELECT COUNT(*) FROM users") == 0


@pytest.mark.unit
def test_with_connection_wrapper_injects_connection(sqlite_users_connection):
    @with_connection(lambda: sqlite_users_connection)
    def count_users(*, connection: sqlite3.Connection) -> int:
        return int(fetch_value(connection, "SELECT COUNT(*) FROM users"))

    assert count_users() == 0


@pytest.mark.unit
def test_transactional_wrapper_commits_on_success(tmp_path):
    db_path = tmp_path / "demo.sqlite"
    with sqlite3.connect(db_path) as connection:
        _create_users_table(connection)

    @transactional(lambda: sqlite3.connect(db_path))
    def insert_user(name: str, *, connection: sqlite3.Connection) -> None:
        execute_sql(connection, "INSERT INTO users (name) VALUES (?)", (name,))

    insert_user("Ada")

    with sqlite3.connect(db_path) as connection:
        assert fetch_value(connection, "SELECT COUNT(*) FROM users") == 1
