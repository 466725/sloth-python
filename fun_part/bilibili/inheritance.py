"""
Created on 2017-04-01
@author: weipengzheng
"""


class Person:
    def __init__(self, name):
        self.name = name

    def reveal_ID(self):
        print(f"My Name is: {self.name}")


class Hero(Person):
    def __init__(self, name, hero_name):
        super().__init__(name)
        self.hero_name = hero_name

    def reveal_ID(self):
        super().reveal_ID()
        print(f"... And I'm: {self.hero_name}")


andy = Hero("Serena", "Andy")
andy.reveal_ID()
