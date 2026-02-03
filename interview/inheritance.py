'''
Created on 2017-04-01
@author: weipengzheng
'''


class Person(object):
    def __init__(self, name):
        self.name = name

    def reveal_ID(self):
        print("My Name is: {}".format(self.name))


class Hero(Person):
    def __init__(self, name, hero_name):
        super(Hero, self).__init__(name)
        self.hero_name = hero_name

    def reveal_ID(self):
        super(Hero, self).reveal_ID()
        print("... And I'm: {}".format(self.hero_name))


Andy = Hero('Serena', 'Andy')
Andy.reveal_ID()