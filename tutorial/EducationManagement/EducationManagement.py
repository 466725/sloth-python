from tutorial.EducationManagement.Student import Student

class EducationManagement:
    system_version = "1.0.0"
    system_name = "Education Management System"
    MIN_SCORE = 0
    MAX_SCORE = 100

    def __init__(self):
        self.students_list = []

    def _find_student(self, name):
        """Helper to find a student by name."""
        return next((s for s in self.students_list if s.name == name), None)

    def add_student(self, name, age, score):
        if self._find_student(name):
            print("Student already exists!")
            return False
        if not (self.MIN_SCORE <= score <= self.MAX_SCORE) or age < 0:
            print("Invalid input values!")
            return False

        self.students_list.append(Student(name, age, score))
        print("Student added successfully!")
        return True

    def remove_student(self, name):
        student = self._find_student(name)
        if student:
            self.students_list.remove(student)
            print("Student removed successfully!")
            return True
        print("Student not found!")
        return False

    def update_student_score(self, name, score):
        if not (self.MIN_SCORE <= score <= self.MAX_SCORE):
            print("Invalid score!")
            return False
        student = self._find_student(name)
        if student:
            student.update_score(score)
            print("Score updated successfully!")
            return True
        print("Student not found!")
        return False

    def get_student_count(self):
        return len(self.students_list)

    def run(self):
        print(f"Welcome to {self.system_name}! Version: {self.system_version}")
        while True:
            print("\n" + "#" * 48 + "\nMenu:")
            print("1. Add student\n2. Remove student\n3. Update student score\n4. Get student count\n5. Exit")
            print("#" * 48)

            try:
                choice = int(input("Enter your choice: "))
                match choice:
                    case 1:
                        name = input("Enter student name: ")
                        age = int(input("Enter student age: "))
                        score = int(input("Enter student score: "))
                        self.add_student(name, age, score)
                    case 2:
                        name = input("Enter student name: ")
                        self.remove_student(name)
                    case 3:
                        name = input("Enter student name: ")
                        score = int(input("Enter student score: "))
                        self.update_student_score(name, score)
                    case 4:
                        print(f"Total students: {self.get_student_count()}")
                    case 5:
                        print(f"Exiting {self.system_name}...")
                        break
                    case _:
                        print("Invalid choice! Please try again.")
            except ValueError:
                print("Error: Please enter numeric values where required.")

#test
if __name__ == "__main__":
    em = EducationManagement()
    em.run()