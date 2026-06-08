"""
Small MySQL demo script: connect and print all tables in a schema.

Default values match the Java example provided by the project owner.
"""

from __future__ import annotations

import argparse
import os
from typing import Iterable

import mysql.connector
from mysql.connector import Error


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3306
DEFAULT_DB = "slothdb"
DEFAULT_USER = "slothuser"
DEFAULT_PASSWORD = "slothpass123"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Connect to MySQL and print tables from one schema.")
    parser.add_argument("--host", default=os.getenv("SLOTH_MYSQL_HOST", DEFAULT_HOST))
    parser.add_argument("--port", type=int, default=int(os.getenv("SLOTH_MYSQL_PORT", str(DEFAULT_PORT))))
    parser.add_argument("--database", default=os.getenv("SLOTH_MYSQL_DB", DEFAULT_DB))
    parser.add_argument("--user", default=os.getenv("SLOTH_MYSQL_USER", DEFAULT_USER))
    parser.add_argument("--password", default=os.getenv("SLOTH_MYSQL_PASSWORD", DEFAULT_PASSWORD))
    return parser


def show_tables(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    database: str = DEFAULT_DB,
    user: str = DEFAULT_USER,
    password: str = DEFAULT_PASSWORD,
) -> list[str]:
    """Return table names from the given MySQL schema."""
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            rows: Iterable[tuple[str]] = cursor.fetchall()
            return [row[0] for row in rows]
    finally:
        conn.close()


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
    except Error as exc:
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
