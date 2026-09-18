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

# Get a DB connection using a configuration object.
def get_connection(config):
    """Get a database connection using the provided configuration object.

    Args:
        config: A configuration object containing database connection parameters.

    Returns:
        connection: A database connection object.
    """
    return create_connection(
        server=config.server,
        database=config.database,
        user=config.user,
        password=config.password
    )  

# Close a DB connection.
def close_connection(connection):
    """Close the provided database connection.

    Args:
        connection: The database connection object to close.
    """
    if connection:
        connection.close()

# Query one record from the database using a SQL query and optional parameters.
def query_one(connection, query, params=None):
    """Query one record from the database using the provided SQL query and optional parameters.

    Args:
        connection: The database connection object.
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to pass to the query.

    Returns:
        tuple: A single row returned by the query, or None if no row is found.
    """
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()

# Query all records from the database using a SQL query and optional parameters.
def query_all(connection, query, params=None):
    """Query all records from the database using the provided SQL query and optional parameters.

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
        return cursor.fetchall()
    finally:
        cursor.close()

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