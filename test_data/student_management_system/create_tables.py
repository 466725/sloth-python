from utils.data_base.sql_queries import STUDENT_MANAGEMENT_SCHEMA 
# Run this script to create tables and populate them with initial data, here is the command: 
"""
python -c "from utils.data_base import connect_mysql; from test_data.student_management_system.create_tables import create_tables; connection=connect_mysql(); cursor=connection.cursor(); create_tables(cursor); connection.commit(); cursor.close(); connection.close()"
"""
# Make sure to have the database connection ready before running this script. And no need to run it multiple times.

DEPARTMENTS = (
    ("CS", "Computer Science"),
    ("BUS", "Business Administration"),
    ("ENG", "Engineering"),
    ("MAT", "Mathematics"),
    ("BIO", "Biology"),
    ("ART", "Fine Arts"),
)

BRANCHES = (
    (1, "Corporate", 206),
    (2, "Sales", 207),
    (3, "Information Technology", 208),
)

EMPLOYEES = (
    (206, "Maya Chen", "1988-04-16", "F", 92000, 1, None),
    (207, "Daniel Brooks", "1985-07-03", "M", 68000, 2, 206),
    (208, "Priya Shah", "1990-12-06", "F", 75000, 3, 206),
    (209, "Marcus Reed", "1993-10-22", "M", 64000, 3, 207),
    (210, "Elena Morales", "1982-08-17", "F", 105000, 1, 207),
)

CLIENTS = (
    (400, "Northstar Logistics", "+1-416-555-0140"),
    (401, "Greenfield Market", "+1-416-555-0141"),
    (402, "Apex Manufacturing", "+1-416-555-0142"),
    (403, "Riverside Health", "+1-416-555-0143"),
    (404, "Summit Retail Group", "+1-416-555-0144"),
)

WORK_WITH = (
    (206, 400, 70000),
    (207, 401, 24000),
    (208, 402, 9800),
    (208, 403, 24000),
    (210, 404, 87900),
)

INSTRUCTORS = (
    ("EMP-1001", "Ada", "Lovelace", "ada.lovelace@example.edu", "CS"),
    ("EMP-1002", "Alan", "Turing", "alan.turing@example.edu", "CS"),
    ("EMP-1003", "Grace", "Hopper", "grace.hopper@example.edu", "ENG"),
    ("EMP-1004", "Katherine", "Johnson", "katherine.johnson@example.edu", "MAT"),
    ("EMP-1005", "George", "Washington", "george.washington@example.edu", "BUS"),
    ("EMP-1006", "Rachel", "Carson", "rachel.carson@example.edu", "BIO"),
    ("EMP-1007", "Maya", "Angelou", "maya.angelou@example.edu", "ART"),
    ("EMP-1008", "Nikola", "Tesla", "nikola.tesla@example.edu", "ENG"),
)

STUDENTS = tuple(
    (
        f"STU-{number:04d}",
        first_name,
        last_name,
        f"{first_name.lower()}.{last_name.lower()}@example.edu",
        date_of_birth,
        department_code,
        status,
    )
    for number, first_name, last_name, date_of_birth, department_code, status in (
        (1, "Sofia", "Anderson", "2003-02-14", "CS", "ACTIVE"),
        (2, "Liam", "Bennett", "2002-11-09", "ENG", "ACTIVE"),
        (3, "Olivia", "Carter", "2004-06-22", "BUS", "ACTIVE"),
        (4, "Noah", "Davis", "2001-08-30", "MAT", "GRADUATED"),
        (5, "Emma", "Evans", "2003-01-17", "BIO", "ACTIVE"),
        (6, "Mateo", "Foster", "2002-04-05", "ART", "ACTIVE"),
        (7, "Ava", "Garcia", "2004-09-12", "CS", "ACTIVE"),
        (8, "Ethan", "Harris", "2000-12-03", "ENG", "GRADUATED"),
        (9, "Mia", "Irwin", "2003-05-28", "BUS", "ACTIVE"),
        (10, "Lucas", "Jackson", "2002-07-19", "MAT", "INACTIVE"),
        (11, "Isabella", "King", "2004-03-11", "BIO", "ACTIVE"),
        (12, "James", "Lewis", "2001-10-26", "ART", "GRADUATED"),
        (13, "Amelia", "Martin", "2003-12-08", "CS", "ACTIVE"),
        (14, "Henry", "Nelson", "2002-02-21", "ENG", "ACTIVE"),
        (15, "Harper", "Owens", "2004-08-16", "BUS", "ACTIVE"),
        (16, "Benjamin", "Parker", "2001-06-07", "MAT", "GRADUATED"),
        (17, "Evelyn", "Quinn", "2003-04-29", "BIO", "ACTIVE"),
        (18, "Alexander", "Roberts", "2002-09-24", "ART", "ACTIVE"),
        (19, "Luna", "Stewart", "2004-01-13", "CS", "ACTIVE"),
        (20, "Daniel", "Turner", "2000-05-02", "ENG", "GRADUATED"),
        (21, "Camila", "Underwood", "2003-07-15", "BUS", "ACTIVE"),
        (22, "Michael", "Vasquez", "2002-11-27", "MAT", "INACTIVE"),
        (23, "Eleanor", "White", "2004-10-04", "BIO", "ACTIVE"),
        (24, "Sebastian", "Young", "2001-03-18", "ART", "GRADUATED"),
    )
)

COURSES = (
    ("CS101", "Introduction to Programming", 3, "CS", "EMP-1001"),
    ("CS205", "Data Structures", 4, "CS", "EMP-1002"),
    ("BUS110", "Principles of Management", 3, "BUS", "EMP-1005"),
    ("BUS220", "Business Analytics", 3, "BUS", "EMP-1005"),
    ("ENG120", "Engineering Design", 4, "ENG", "EMP-1003"),
    ("ENG240", "Electrical Systems", 4, "ENG", "EMP-1008"),
    ("MAT101", "College Algebra", 3, "MAT", "EMP-1004"),
    ("MAT210", "Applied Statistics", 3, "MAT", "EMP-1004"),
    ("BIO105", "Foundations of Biology", 4, "BIO", "EMP-1006"),
    ("BIO230", "Ecology", 3, "BIO", "EMP-1006"),
    ("ART115", "Drawing Fundamentals", 3, "ART", "EMP-1007"),
    ("ART205", "Digital Media Studio", 3, "ART", "EMP-1007"),
)

ENROLLMENTS = (
    (f"STU-{student_number:04d}", course_code, academic_year, term, status, grade)
    for student_number, course_code, academic_year, term, status, grade in (
        (1, "CS101", "2024-2025", "FALL", "COMPLETED", "A"),
        (1, "MAT101", "2024-2025", "FALL", "COMPLETED", "A-"),
        (1, "CS205", "2024-2025", "SPRING", "ENROLLED", None),
        (2, "ENG120", "2024-2025", "FALL", "COMPLETED", "B+"),
        (2, "MAT101", "2024-2025", "FALL", "COMPLETED", "B"),
        (2, "ENG240", "2024-2025", "SPRING", "ENROLLED", None),
        (3, "BUS110", "2024-2025", "FALL", "COMPLETED", "A-"),
        (3, "BUS220", "2024-2025", "SPRING", "ENROLLED", None),
        (4, "MAT210", "2023-2024", "FALL", "COMPLETED", "A"),
        (4, "CS101", "2023-2024", "SPRING", "COMPLETED", "B+"),
        (5, "BIO105", "2024-2025", "FALL", "COMPLETED", "A"),
        (5, "BIO230", "2024-2025", "SPRING", "ENROLLED", None),
        (6, "ART115", "2024-2025", "FALL", "COMPLETED", "B+"),
        (6, "ART205", "2024-2025", "SPRING", "ENROLLED", None),
        (7, "CS101", "2024-2025", "FALL", "COMPLETED", "A-"),
        (7, "CS205", "2024-2025", "SPRING", "ENROLLED", None),
        (8, "ENG120", "2022-2023", "FALL", "COMPLETED", "A"),
        (8, "ENG240", "2022-2023", "SPRING", "COMPLETED", "A-"),
        (9, "BUS110", "2024-2025", "FALL", "COMPLETED", "B"),
        (9, "BUS220", "2024-2025", "SPRING", "ENROLLED", None),
        (10, "MAT101", "2023-2024", "FALL", "DROPPED", None),
        (11, "BIO105", "2024-2025", "FALL", "COMPLETED", "B+"),
        (11, "MAT101", "2024-2025", "SPRING", "ENROLLED", None),
        (12, "ART115", "2022-2023", "FALL", "COMPLETED", "A"),
        (12, "ART205", "2022-2023", "SPRING", "COMPLETED", "A-"),
        (13, "CS101", "2024-2025", "FALL", "COMPLETED", "A"),
        (13, "CS205", "2024-2025", "SPRING", "ENROLLED", None),
        (14, "ENG120", "2024-2025", "FALL", "COMPLETED", "B"),
        (14, "MAT210", "2024-2025", "SPRING", "ENROLLED", None),
        (15, "BUS110", "2024-2025", "FALL", "COMPLETED", "A-"),
        (15, "MAT210", "2024-2025", "SPRING", "ENROLLED", None),
        (16, "MAT101", "2022-2023", "FALL", "COMPLETED", "A"),
        (16, "MAT210", "2022-2023", "SPRING", "COMPLETED", "A"),
        (17, "BIO105", "2024-2025", "FALL", "COMPLETED", "A-"),
        (17, "BIO230", "2024-2025", "SPRING", "ENROLLED", None),
        (18, "ART115", "2024-2025", "FALL", "COMPLETED", "B"),
        (18, "ART205", "2024-2025", "SPRING", "ENROLLED", None),
        (19, "CS101", "2024-2025", "FALL", "COMPLETED", "B+"),
        (19, "BUS110", "2024-2025", "SPRING", "ENROLLED", None),
        (20, "ENG240", "2022-2023", "FALL", "COMPLETED", "A"),
        (20, "MAT210", "2022-2023", "SPRING", "COMPLETED", "B+"),
        (21, "BUS220", "2024-2025", "FALL", "COMPLETED", "A-"),
        (21, "CS101", "2024-2025", "SPRING", "ENROLLED", None),
        (22, "MAT101", "2023-2024", "FALL", "DROPPED", None),
        (23, "BIO105", "2024-2025", "FALL", "COMPLETED", "A"),
        (23, "ART115", "2024-2025", "SPRING", "ENROLLED", None),
        (24, "ART205", "2022-2023", "FALL", "COMPLETED", "A"),
        (24, "BUS110", "2022-2023", "SPRING", "COMPLETED", "B+"),
    )
)


def _id_by_value(cursor, table_name, column_name, value):
    cursor.execute(f"SELECT id FROM {table_name} WHERE {column_name} = %s", (value,))
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(f"Could not find {table_name}.{column_name}={value!r} after insert")
    return row[0]


def seed_data(cursor):
    cursor.executemany(
        "INSERT IGNORE INTO departments (code, name) VALUES (%s, %s)", DEPARTMENTS
    )
    department_ids = {
        code: _id_by_value(cursor, "departments", "code", code) for code, _ in DEPARTMENTS
    }

    cursor.executemany(
        "INSERT IGNORE INTO branches (branch_id, branch_name, manager_id) VALUES (%s, %s, %s)",
        BRANCHES,
    )
    cursor.executemany(
        """
        INSERT IGNORE INTO employees
            (emp_id, name, birth_date, sex, salary, branch_id, sup_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        EMPLOYEES,
    )
    cursor.executemany(
        "INSERT IGNORE INTO clients (client_id, client_name, phone) VALUES (%s, %s, %s)",
        CLIENTS,
    )
    cursor.executemany(
        "INSERT IGNORE INTO work_with (emp_id, client_id, total_sales) VALUES (%s, %s, %s)",
        WORK_WITH,
    )

    cursor.executemany(
        """
        INSERT IGNORE INTO instructors
            (employee_number, first_name, last_name, email, department_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (employee_number, first_name, last_name, email, department_ids[department_code])
            for employee_number, first_name, last_name, email, department_code in INSTRUCTORS
        ],
    )
    cursor.executemany(
        """
        INSERT IGNORE INTO students
            (student_number, first_name, last_name, email, date_of_birth, department_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        [
            (student_number, first_name, last_name, email, date_of_birth, department_ids[department_code], status)
            for student_number, first_name, last_name, email, date_of_birth, department_code, status in STUDENTS
        ],
    )

    instructor_ids = {
        employee_number: _id_by_value(cursor, "instructors", "employee_number", employee_number)
        for employee_number, *_ in INSTRUCTORS
    }
    cursor.executemany(
        """
        INSERT IGNORE INTO courses
            (course_code, title, credits, department_id, instructor_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (course_code, title, credits, department_ids[department_code], instructor_ids[employee_number])
            for course_code, title, credits, department_code, employee_number in COURSES
        ],
    )

    student_ids = {
        student_number: _id_by_value(cursor, "students", "student_number", student_number)
        for student_number, *_ in STUDENTS
    }
    course_ids = {
        course_code: _id_by_value(cursor, "courses", "course_code", course_code)
        for course_code, *_ in COURSES
    }
    cursor.executemany(
        """
        INSERT IGNORE INTO enrollments
            (student_id, course_id, academic_year, term, status, grade)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        [
            (student_ids[student_number], course_ids[course_code], academic_year, term, status, grade)
            for student_number, course_code, academic_year, term, status, grade in ENROLLMENTS
        ],
    )


def create_tables(cursor, *, seed=True):
    for query in STUDENT_MANAGEMENT_SCHEMA:
        cursor.execute(query)
    if seed:
        seed_data(cursor)

