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

# Serena = Person('Serena')
# Serena.reveal_ID()
Andy = Hero('Serena', 'Andy')
Andy.reveal_ID()

class A(object):
    def go(self):
        print("go A go!")
    def stop(self):
        print("stop A stop!")
    def pause(self):
        raise Exception("Not Implemented")

class B(A):
    def go(self):
        super(B, self).go()
        print("go B go!")

class C(A):
    def go(self):
        super(C, self).go()
        print("go C go!")
    def stop(self):
        super(C, self).stop()
        print("stop C stop!")

class D(B, C):
    def go(self):
        super(D, self).go()
        print("go D go!")
    def stop(self):
        super(D, self).stop()
        print("stop D stop!")
    def pause(self):
        print("wait D wait!")

class E(B, C): pass

a = A()
b = B()
c = C()
d = D()
e = E()

# specify output from here onwards
a.go()
b.go()
c.go()
d.go()
e.go()
a.stop()
b.stop()
c.stop()
d.stop()
e.stop()
# a.pause()
# b.pause()
# c.pause()
# d.pause()
# e.pause()

class Node(object):
    def __init__(self, sName):
        self._lChildren = []
        self.sName = sName
    def __repr__(self):
        return "<Node '{}'>".format(self.sName)
    def append(self, *args, **kwargs):
        self._lChildren.append(*args, **kwargs)
    def print_all_1(self):
        print(self)
        for oChild in self._lChildren:
            oChild.print_all_1()
    def print_all_2(self):
        def gen(o):
            lAll = [o, ]
            while lAll:
                oNext = lAll.pop(0)
                lAll.extend(oNext._lChildren)
                yield oNext
        for oNode in gen(self):
            print(oNode)
oRoot = Node("root")
oChild1 = Node("child1")
oChild2 = Node("child2")
oChild3 = Node("child3")
oChild4 = Node("child4")
oChild5 = Node("child5")
oChild6 = Node("child6")
oChild7 = Node("child7")
oChild8 = Node("child8")
oChild9 = Node("child9")
oChild10 = Node("child10")
oRoot.append(oChild1)
oRoot.append(oChild2)
oRoot.append(oChild3)
oChild1.append(oChild4)
oChild1.append(oChild5)
oChild2.append(oChild6)
oChild4.append(oChild7)
oChild3.append(oChild8)
oChild3.append(oChild9)
oChild6.append(oChild10)

# specify output from here onwards
oRoot.print_all_1()
oRoot.print_all_2()
