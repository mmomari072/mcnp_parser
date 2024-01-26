# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:55:56 2024

@author: mohammed.omari
"""

class str2num:
    def __init__(self,x:str,return_type=int):
        self.x = x
        self.return_type = return_type
        self.converted_value = None
    def IsType(self,return_type=int):
        try:
            self.converted_value= self.return_type(self.x)
            return True
        except:
            return False
    def convert(self):
        if self.IsType():
            return self.converted_value
        return None

def Split_txt(x:str, without_blanks=True):
    if without_blanks:
        return [s for s in x.split() if s !='']
    return [s for s in x.split()]
            