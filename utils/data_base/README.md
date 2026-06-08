# Database Utilities

`utils.data_base` provides small, reusable helpers for database code:

- `DatabaseConfig.from_env()` loads MySQL connection settings.
- `connect_mysql()` opens a MySQL connection.
- `connection_scope()` safely opens, commits, rolls back, and closes connections.
- `cursor_scope()` gives direct cursor access when custom SQL handling is needed.
- `execute_sql()`, `fetch_one()`, `fetch_all()`, and `fetch_value()` cover common SQL calls.
- `with_connection()` and `transactional()` wrap functions with managed connections.

## MySQL Environment Variables

```env
SLOTH_MYSQL_HOST=localhost
SLOTH_MYSQL_PORT=3306
SLOTH_MYSQL_DB=slothdb
SLOTH_MYSQL_USER=slothuser
SLOTH_MYSQL_PASSWORD=replace-with-local-password
```

## Parameterized SQL

```python
from utils.data_base import connect_mysql, execute_sql, fetch_all

connection = connect_mysql()
try:
    execute_sql(
        connection,
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("Ada Lovelace", "ada@example.com"),
        commit=True,
    )
    rows = fetch_all(connection, "SELECT id, name FROM users WHERE email = %s", ("ada@example.com",))
finally:
    connection.close()
```

## Cursor Usage

```python
from utils.data_base import connect_mysql, cursor_scope

connection = connect_mysql()
try:
    with cursor_scope(connection, dictionary=True) as cursor:
        cursor.execute("SELECT id, name FROM users")
        for row in cursor:
            print(row["name"])
finally:
    connection.close()
```

## Transaction Wrapper

```python
from utils.data_base import connect_mysql, execute_sql, transactional


@transactional(connect_mysql)
def create_user(name: str, email: str, *, connection):
    execute_sql(
        connection,
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email),
    )
```

For runnable SQLite examples that do not need a server, run:

```powershell
python -m utils.data_base.examples
```
