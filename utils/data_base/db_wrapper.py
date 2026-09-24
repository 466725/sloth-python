"""Reusable wrappers for MySQL and DB-API compatible connections."""

from __future__ import annotations

import functools
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from typing import Any, ParamSpec, TypeVar

from config.config import DatabaseSettings, settings

DatabaseConfig = DatabaseSettings
SqlParams = Sequence[Any] | Mapping[str, Any] | None
ConnectionFactory = Callable[[], Any]
P = ParamSpec("P")
R = TypeVar("R")


def connect_mysql(config: DatabaseConfig | None = None, **overrides: Any) -> Any:
    """Open a MySQL connection using the configured local database settings."""

    try:
        import mysql.connector
    except ImportError as exc:
        raise RuntimeError(
            "mysql-connector-python is required for MySQL connections. "
            "Install project dependencies with: pip install -r requirements.txt"
        ) from exc

    resolved = config or settings.database
    kwargs = resolved.as_mysql_kwargs()
    kwargs.update(overrides)
    return mysql.connector.connect(**kwargs)


@contextmanager
def connection_scope(
    connection_factory: ConnectionFactory,
    *,
    commit: bool = False,
    rollback_on_error: bool = True,
    close: bool = True,
) -> Iterator[Any]:
    """Open a connection for a block, optionally commit, and always close it."""

    connection = connection_factory()
    try:
        yield connection
        if commit:
            connection.commit()
    except Exception:
        if rollback_on_error and hasattr(connection, "rollback"):
            connection.rollback()
        raise
    finally:
        if close:
            connection.close()


@contextmanager
def cursor_scope(connection: Any, **cursor_kwargs: Any) -> Iterator[Any]:
    """Create a cursor and close it after use."""

    cursor = connection.cursor(**cursor_kwargs) if cursor_kwargs else connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def execute_sql(
    connection: Any,
    sql: str,
    params: SqlParams = None,
    *,
    many: bool = False,
    commit: bool = False,
) -> int:
    """Run DDL or DML and return the affected row count."""

    with cursor_scope(connection) as cursor:
        if many:
            cursor.executemany(sql, params or [])
        else:
            cursor.execute(sql, params or ())
        rowcount = cursor.rowcount

    if commit:
        connection.commit()
    return rowcount


def fetch_all(
    connection: Any,
    sql: str,
    params: SqlParams = None,
    *,
    as_dict: bool = False,
) -> list[Any]:
    """Run a query and return all rows."""

    cursor_kwargs = {"dictionary": True} if as_dict else {}
    with cursor_scope(connection, **cursor_kwargs) as cursor:
        cursor.execute(sql, params or ())
        return list(cursor.fetchall())


def fetch_one(
    connection: Any,
    sql: str,
    params: SqlParams = None,
    *,
    as_dict: bool = False,
) -> Any | None:
    """Run a query and return one row, or ``None`` when no row matches."""

    cursor_kwargs = {"dictionary": True} if as_dict else {}
    with cursor_scope(connection, **cursor_kwargs) as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchone()


def fetch_value(connection: Any, sql: str, params: SqlParams = None, default: Any = None) -> Any:
    """Run a query and return the first value from its first row."""

    row = fetch_one(connection, sql, params)
    if row is None:
        return default
    if isinstance(row, Mapping):
        return next(iter(row.values()), default)
    return row[0] if row else default


def with_connection(
    connection_factory: ConnectionFactory,
    *,
    commit: bool = False,
    connection_arg: str = "connection",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorate a function to inject a managed connection keyword argument."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if connection_arg in kwargs and kwargs[connection_arg] is not None:
                return func(*args, **kwargs)

            with connection_scope(connection_factory, commit=commit) as connection:
                kwargs[connection_arg] = connection
                return func(*args, **kwargs)

        return wrapper

    return decorator


def transactional(connection_factory: ConnectionFactory) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorate a function to commit on success and roll back on error."""

    return with_connection(connection_factory, commit=True)


def show_tables(connection: Any) -> list[str]:
    """Return the table names visible to an open database connection."""

    return [row[0] for row in fetch_all(connection, "SHOW TABLES")]


def create_connection(
    server: str | None = None,
    database: str | None = None,
    user: str | None = None,
    password: str | None = None,
    port: int | None = None,
) -> Any:
    """Open a MySQL connection with optional setting overrides."""

    overrides = {
        key: value
        for key, value in {
            "host": server,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }.items()
        if value is not None
    }
    return connect_mysql(settings.database, **overrides)


def get_connection(config: DatabaseConfig) -> Any:
    """Open a MySQL connection from a ``DatabaseConfig`` instance."""

    return connect_mysql(config)


def close_connection(connection: Any) -> None:
    """Close a connection when one was created."""

    if connection is not None:
        connection.close()


def query_one(connection: Any, query: str, params: SqlParams = None) -> Any | None:
    """Compatibility wrapper for ``fetch_one``."""

    return fetch_one(connection, query, params)


def query_all(connection: Any, query: str, params: SqlParams = None) -> list[Any]:
    """Compatibility wrapper for ``fetch_all``."""

    return fetch_all(connection, query, params)


def execute_query(connection: Any, query: str, params: SqlParams = None) -> list[Any] | None:
    """Execute a query, returning rows for SELECT statements and committing writes."""

    if query.lstrip().upper().startswith("SELECT"):
        return fetch_all(connection, query, params)

    execute_sql(connection, query, params, commit=True)
    return None