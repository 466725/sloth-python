"""Reusable database helpers for DB-API compatible Python drivers.

The package is intentionally small, but covers the common professional patterns:

- load connection settings from environment variables
- open and close connections safely
- run parameterized SQL
- use cursors directly when custom logic is needed
- wrap work in a transaction

The MySQL helpers use ``mysql-connector-python``. The generic helpers work with
any PEP 249 / DB-API style connection, including ``sqlite3``.
"""

from __future__ import annotations

import argparse
import functools
import os
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, ParamSpec, TypeVar


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3306
DEFAULT_DB = "slothdb"
DEFAULT_USER = "slothuser"
DEFAULT_PASSWORD = "slothpass123"

SqlParams = Sequence[Any] | Mapping[str, Any] | None
ConnectionFactory = Callable[[], Any]
P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class DatabaseConfig:
    """Connection settings for a MySQL database."""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    database: str = DEFAULT_DB
    user: str = DEFAULT_USER
    password: str = DEFAULT_PASSWORD

    @classmethod
    def from_env(cls, prefix: str = "SLOTH_MYSQL") -> "DatabaseConfig":
        """Build config from environment variables.

        For the default prefix, the variables are:
        ``SLOTH_MYSQL_HOST``, ``SLOTH_MYSQL_PORT``, ``SLOTH_MYSQL_DB``,
        ``SLOTH_MYSQL_USER``, and ``SLOTH_MYSQL_PASSWORD``.
        """

        return cls(
            host=os.getenv(f"{prefix}_HOST", DEFAULT_HOST),
            port=int(os.getenv(f"{prefix}_PORT", str(DEFAULT_PORT))),
            database=os.getenv(f"{prefix}_DB", DEFAULT_DB),
            user=os.getenv(f"{prefix}_USER", DEFAULT_USER),
            password=os.getenv(f"{prefix}_PASSWORD", DEFAULT_PASSWORD),
        )

    def as_mysql_kwargs(self) -> dict[str, Any]:
        """Return keyword arguments accepted by ``mysql.connector.connect``."""

        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
        }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Connect to MySQL and print tables from one schema.")
    config = DatabaseConfig.from_env()
    parser.add_argument("--host", default=config.host)
    parser.add_argument("--port", type=int, default=config.port)
    parser.add_argument("--database", default=config.database)
    parser.add_argument("--user", default=config.user)
    parser.add_argument("--password", default=config.password)
    return parser


def connect_mysql(config: DatabaseConfig | None = None, **overrides: Any) -> Any:
    """Open a MySQL connection.

    ``overrides`` can pass any extra option supported by ``mysql.connector``, such
    as ``autocommit=True`` or ``connection_timeout=10``.
    """

    try:
        import mysql.connector
    except ImportError as exc:
        raise RuntimeError(
            "mysql-connector-python is required for MySQL connections. "
            "Install project dependencies with: pip install -r requirements.txt"
        ) from exc

    resolved = config or DatabaseConfig.from_env()
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
    """Open a connection for a block and close it safely.

    Set ``commit=True`` for write operations. On exceptions, the helper rolls the
    transaction back when the connection supports ``rollback``.
    """

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
    """Create a cursor and close it after use.

    MySQL accepts keyword arguments such as ``dictionary=True``. Some drivers,
    including ``sqlite3``, do not accept cursor kwargs; for those drivers call
    this helper without kwargs.
    """

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
    """Run INSERT/UPDATE/DELETE or DDL SQL and return affected row count.

    Use placeholders appropriate for your driver. For MySQL connector use ``%s``;
    for sqlite3 use ``?``.
    """

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
    """Run a SELECT query and return all rows."""

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
    """Run a SELECT query and return one row, or ``None`` when no row matches."""

    cursor_kwargs = {"dictionary": True} if as_dict else {}
    with cursor_scope(connection, **cursor_kwargs) as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchone()


def fetch_value(connection: Any, sql: str, params: SqlParams = None, default: Any = None) -> Any:
    """Run a SELECT query and return the first column from the first row."""

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
    """Decorator that injects a managed connection into a function.

    The wrapped function should accept a keyword argument named ``connection`` by
    default. Change ``connection_arg`` if your function uses another name.
    """

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
    """Decorator for functions that should commit on success and rollback on error."""

    return with_connection(connection_factory, commit=True)


def show_tables(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    database: str = DEFAULT_DB,
    user: str = DEFAULT_USER,
    password: str = DEFAULT_PASSWORD,
) -> list[str]:
    """Return table names from the given MySQL schema."""
    config = DatabaseConfig(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )
    with connection_scope(lambda: connect_mysql(config)) as conn:
        with cursor_scope(conn) as cursor:
            cursor.execute("SHOW TABLES")
            rows: Iterable[tuple[str]] = cursor.fetchall()
            return [row[0] for row in rows]


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    try:
        tables = show_tables(
            host=args.host,
            port=args.port,
            database=args.database,
            user=args.user,
            password=args.password,
        )
    except Exception as exc:
        print(f"MySQL connection/query failed: {exc}")
        return 1

    print(f"Tables in {args.database}:")
    if not tables:
        print("- (no tables found)")
    else:
        for table in tables:
            print(f"- {table}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
