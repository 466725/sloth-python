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

GET_ACTIVE_USER_BY_NAME = """
    SELECT name, active
    FROM `{table_name}`
    WHERE name = %s
    LIMIT 1;
"""

ENROLL_STUDENT_IN_COURSE = """
    INSERT INTO enrollments (student_id, course_id, academic_year, term)
    SELECT s.id, c.id, %s, %s
    FROM students s
    INNER JOIN courses c
    WHERE s.student_number = %s
        AND s.status = 'ACTIVE'
        AND c.course_code = %s;
"""

CREATE_DEPARTMENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS departments (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        code VARCHAR(20) NOT NULL UNIQUE,
        name VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
"""

CREATE_STUDENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS students (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        student_number VARCHAR(30) NOT NULL UNIQUE,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        date_of_birth DATE NULL,
        department_id BIGINT UNSIGNED NULL,
        status ENUM('ACTIVE', 'INACTIVE', 'GRADUATED') NOT NULL DEFAULT 'ACTIVE',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
    ) ENGINE=InnoDB;
"""

CREATE_INSTRUCTORS_TABLE = """
    CREATE TABLE IF NOT EXISTS instructors (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        employee_number VARCHAR(30) NOT NULL UNIQUE,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        department_id BIGINT UNSIGNED NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
    ) ENGINE=InnoDB;
"""

CREATE_COURSES_TABLE = """
    CREATE TABLE IF NOT EXISTS courses (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        course_code VARCHAR(30) NOT NULL UNIQUE,
        title VARCHAR(200) NOT NULL,
        credits TINYINT UNSIGNED NOT NULL,
        department_id BIGINT UNSIGNED NULL,
        instructor_id BIGINT UNSIGNED NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
        FOREIGN KEY (instructor_id) REFERENCES instructors(id) ON DELETE SET NULL
    ) ENGINE=InnoDB;
"""

CREATE_ENROLLMENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS enrollments (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        student_id BIGINT UNSIGNED NOT NULL,
        course_id BIGINT UNSIGNED NOT NULL,
        academic_year CHAR(9) NOT NULL,
        term ENUM('SPRING', 'SUMMER', 'FALL', 'WINTER') NOT NULL,
        status ENUM('ENROLLED', 'DROPPED', 'COMPLETED') NOT NULL DEFAULT 'ENROLLED',
        grade VARCHAR(2) NULL,
        enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_enrollment (student_id, course_id, academic_year, term),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
"""

STUDENT_MANAGEMENT_SCHEMA = (
    CREATE_DEPARTMENTS_TABLE,
    CREATE_STUDENTS_TABLE,
    CREATE_INSTRUCTORS_TABLE,
    CREATE_COURSES_TABLE,
    CREATE_ENROLLMENTS_TABLE,
)
