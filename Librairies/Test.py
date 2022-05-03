# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:15:58 2022

@author: cedri
"""

class parent:
    def __init__(self,children):
        self.children = children
        self.age = 34
        
    def Age(self):
        print('age')
        
class child(parent):
    def __init__(self,children):
        super().__init__(children)
        
    def age2(self):
        print(super().Age())
        print(self.age)
        
        
jules = parent('paul')

jules.Age()

paul = child('jules')

paul.age2()

print(paul.children)
print(paul.age)