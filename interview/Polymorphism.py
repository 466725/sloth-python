class Animal:
    nama = "Animal"
    color = "white"
    def __init__(self, nama, color):
        self.nama = nama
        self.color = color
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        print("Woof!")
    def eat(self):
        print("Dog eat meat! ")

class Cat(Animal):
    def make_sound(self):
        print("Meow!")
    def eat(self):
        print("Cat eat fish! ")

if __name__ == "__main__":
    aninmal = Animal("Animal", "white")

    aninmal = Dog("Rex", "black")
    aninmal.make_sound()
    aninmal.eat()

    aninmal = Cat("Tom", "white")
    aninmal.make_sound()
    aninmal.eat()