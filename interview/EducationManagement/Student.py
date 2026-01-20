"""
Student class
"""


class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __str__(self):
        return f"Student(name = '{self.name}', age = {self.age}, score = {self.score})"

    def update_score(self, score=None):
        if score is not None:
            self.score = score
