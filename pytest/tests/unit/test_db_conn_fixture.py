import pytest

from utils.data_base import execute_sql, fetch_value


@pytest.mark.unit
def test_db_conn_fixture_provides_managed_connection(db_conn):
    execute_sql(
        db_conn,
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """,
    )
    execute_sql(db_conn, "INSERT INTO users (name) VALUES (?)", ("Ada",))

    assert fetch_value(db_conn, "SELECT COUNT(*) FROM users") == 1
