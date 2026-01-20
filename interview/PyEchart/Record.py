class Record:
    def __init__(self, name: str, age: int, gender: str, occupation: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation

    def __str__(self) -> str:
        return f"{self.name}, {self.age}, {self.gender}, {self.occupation}"
