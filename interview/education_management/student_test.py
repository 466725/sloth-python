"""
Student class
"""


class Student:
    def __init__(self, name, age, gender, score):
        self.name = name
        self.age = age
        self.gender = gender
        self.score = score

    def __str__(self):
        return f"Student(name = '{self.name}', age = {self.age}, gender = '{self.gender}', score = {self.score})"

    def update_score(self, score=None):
        if score is not None:
            self.score = score

    def info(self):
        print(self.name, self.age, self.gender, self.score)
        return self.__str__()

stu = Student("Tom", 20, "male", 90)
print(stu.info())

def test_student_info():
    """Test student info method."""
    stu = Student("Jerry", 22, "female", 85)
    assert stu.info() == "Student(name = 'Jerry', age = 22, gender = 'female', score = 85)"

    stu = Student("Alice", 21, "female", 95)
    assert stu.info() == "Student(name = 'Alice', age = 21, gender = 'female', score = 95)"