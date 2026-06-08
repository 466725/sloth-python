"""Small database usage examples.

Run this file directly to see parameterized SQL, cursor usage, and transaction
wrappers with an in-memory SQLite database:

    python -m utils.data_base.examples
"""

from __future__ import annotations

import sqlite3
from typing import Any

from utils.data_base.database_client import (
    connection_scope,
    cursor_scope,
    execute_sql,
    fetch_all,
    fetch_value,
    transactional,
)


def sqlite_connection() -> sqlite3.Connection:
    """Return a SQLite connection for examples and tests."""

    return sqlite3.connect(":memory:")


def create_schema(connection: sqlite3.Connection) -> None:
    execute_sql(
        connection,
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            active INTEGER NOT NULL DEFAULT 1
        )
        """,
    )


def run_sql_with_parameters_example(connection: sqlite3.Connection) -> list[tuple[Any, ...]]:
    """Insert and query rows using parameterized SQL."""

    execute_sql(
        connection,
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Ada Lovelace", "ada@example.com"),
    )
    execute_sql(
        connection,
        "INSERT INTO users (name, email, active) VALUES (?, ?, ?)",
        ("Grace Hopper", "grace@example.com", 0),
    )
    return fetch_all(connection, "SELECT name, email FROM users WHERE active = ?", (1,))


def run_sql_with_cursor_example(connection: sqlite3.Connection) -> list[str]:
    """Use a cursor directly when custom fetch/iteration behavior is needed."""

    names: list[str] = []
    with cursor_scope(connection) as cursor:
        cursor.execute("SELECT name FROM users ORDER BY name")
        for (name,) in cursor:
            names.append(name)
    return names


def wrapper_example() -> int:
    """Show a transaction wrapper that injects a managed connection."""

    connection = sqlite_connection()
    create_schema(connection)

    @transactional(lambda: connection)
    def insert_user(*, connection: sqlite3.Connection) -> int:
        execute_sql(
            connection,
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Katherine Johnson", "katherine@example.com"),
        )
        return fetch_value(connection, "SELECT COUNT(*) FROM users")

    return int(insert_user())


def main() -> None:
    with connection_scope(sqlite_connection, commit=True) as connection:
        create_schema(connection)
        active_users = run_sql_with_parameters_example(connection)
        all_names = run_sql_with_cursor_example(connection)

    print(f"Active users: {active_users}")
    print(f"All names: {all_names}")
    print(f"Wrapper inserted users: {wrapper_example()}")


if __name__ == "__main__":
    main()
