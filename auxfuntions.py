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
        if isinstance(self.x,(list,tuple,set)):
            return(all([str2num(a,return_type).IsType() for a in self.x]))
        try:
            self.converted_value= self.return_type(self.x)
            return True
        except:
            return False
    def convert(self,skip_not_converted=False):
        if self.IsType() and not skip_not_converted:
            if isinstance(self.x, (list,tuple,set)):
                return [str2num(a,self.return_type).convert() for a in self.x]
            return self.converted_value
        elif skip_not_converted:
            if isinstance(self.x, (list,tuple,set)):
                return [str2num(a,self.return_type).convert() for a in self.x]
        return None

def Split_txt(x:str, without_blanks=True):
    if without_blanks:
        return [s for s in x.split() if s !='']
    return [s for s in x.split()]
            


if __name__=="__main__":
    print(str2num(["1","2a"],int).convert(0))