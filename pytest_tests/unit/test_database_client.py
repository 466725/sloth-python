import sqlite3

import pytest

from utils.data_base import (
    DatabaseConfig,
    connection_scope,
    cursor_scope,
    execute_sql,
    fetch_all,
    fetch_one,
    fetch_value,
    transactional,
    with_connection,
)


def _create_connection() -> sqlite3.Connection:
    return sqlite3.connect(":memory:")


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
def test_execute_sql_supports_parameters_and_fetch_helpers():
    connection = _create_connection()
    _create_users_table(connection)

    execute_sql(connection, "INSERT INTO users (name, active) VALUES (?, ?)", ("Ada", 1))
    execute_sql(connection, "INSERT INTO users (name, active) VALUES (?, ?)", ("Grace", 0))

    assert fetch_value(connection, "SELECT COUNT(*) FROM users") == 2
    assert fetch_one(connection, "SELECT name FROM users WHERE active = ?", (1,)) == ("Ada",)
    assert fetch_all(connection, "SELECT name FROM users ORDER BY name") == [("Ada",), ("Grace",)]

    connection.close()


@pytest.mark.unit
def test_execute_sql_supports_many_parameter_sets():
    connection = _create_connection()
    _create_users_table(connection)

    rowcount = execute_sql(
        connection,
        "INSERT INTO users (name, active) VALUES (?, ?)",
        [("Ada", 1), ("Grace", 0), ("Katherine", 1)],
        many=True,
    )

    assert rowcount == 3
    assert fetch_value(connection, "SELECT COUNT(*) FROM users WHERE active = ?", (1,)) == 2

    connection.close()


@pytest.mark.unit
def test_cursor_scope_allows_direct_cursor_usage():
    connection = _create_connection()
    _create_users_table(connection)
    execute_sql(connection, "INSERT INTO users (name) VALUES (?)", ("Ada",))

    with cursor_scope(connection) as cursor:
        cursor.execute("SELECT name FROM users")
        row = cursor.fetchone()

    assert row == ("Ada",)
    connection.close()


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
def test_with_connection_wrapper_injects_connection():
    connection = _create_connection()
    _create_users_table(connection)

    @with_connection(lambda: connection)
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
