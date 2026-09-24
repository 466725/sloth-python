from utils.data_base.sql_queries import STUDENT_MANAGEMENT_SCHEMA 

def create_tables(cursor):
    for query in STUDENT_MANAGEMENT_SCHEMA:
        cursor.execute(query)

