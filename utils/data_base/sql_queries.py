"""SQL query catalog.

Keep SQL statements as named multiline strings. Use placeholders appropriate for
the configured DB-API driver.
"""

GET_ONE_RANDOM_EDITABLE_AE_DETAILS = """
    SELECT ae.id, ae.name, ae.description, ae.created_at, ae.updated_at
    FROM adverse_events ae
    INNER JOIN users u ON ae.created_by = u.id
    WHERE u.role = 'editor'
        AND ae.is_editable = 1
        AND ae.is_active = 1
            AND NOT EXISTS (
                SELECT 1
                FROM adverse_event_restrictions aer
                WHERE aer.adverse_event_id = ?
            )
    ORDER BY RANDOM()
    LIMIT 1;
"""

GET_AE_BY_NAME = """
    SELECT id, name, description, created_at, updated_at
    FROM adverse_events
    WHERE name = ?
    LIMIT 1;
"""

GET_TEST_DATABASE_USER_BY_NAME = """
    SELECT name, active
    FROM `{table_name}`
    WHERE name = %s
    LIMIT 1;
"""