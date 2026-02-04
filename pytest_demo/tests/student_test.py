from interview.education_management.student import Student


def test_student_info():
    """Test student info method."""
    stu = Student("Jerry", 22, "female", 85)
    assert stu.info() == "Student(name = 'Jerry', age = 22, gender = 'female', score = 85)"

    stu = Student("Alice", 21, "female", 95)
    assert stu.info() == "Student(name = 'Alice', age = 21, gender = 'female', score = 95)"
