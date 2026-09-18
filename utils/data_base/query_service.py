"""Application-facing database queries.

This module connects application use cases to the SQL catalog and database
wrapper. Callers provide an open connection and receive database rows; this
module does not create or close connections.
"""

from utils.data_base import db_wrapper, sql_queries


def get_random_editable_adverse_event(connection, excluded_event_id):
    """Return one editable adverse event excluding the specified event."""

    return db_wrapper.query_one(
        connection,
        sql_queries.GET_ONE_RANDOM_EDITABLE_AE_DETAILS,
        (excluded_event_id,),
    )


def get_adverse_event_by_name(connection, name):
    """Return one adverse event matching ``name``, or ``None`` when absent."""

    return db_wrapper.query_one(
        connection,
        sql_queries.GET_AE_BY_NAME,
        (name,),
    )