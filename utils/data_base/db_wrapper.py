# Create a DB connection with server, database, user, and password information.
def create_connection(server, database, user, password):
    """Create a database connection using the provided server, database, user, and password information.

    Args:
        server (str): The database server address.
        database (str): The name of the database.
        user (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        connection: A database connection object.
    """
    import mysql.connector
    return mysql.connector.connect(
        host=server,
        database=database,
        user=user,
        password=password
    )


# Connect to the database and provide a wrapper for executing queries.
# The connection is managed using a context manager to ensure proper cleanup.
def execute_query(connection, query, params=None):
    """Execute a SQL query using the provided database connection.

    Args:
        connection: The database connection object.
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to pass to the query.

    Returns:
        list: A list of rows returned by the query.
    """
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        else:
            connection.commit()
    finally:
        cursor.close()