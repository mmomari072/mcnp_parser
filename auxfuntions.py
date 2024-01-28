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

# 
def Split_txt(x:str, without_blanks=True):
    if without_blanks:
        return [s for s in x.split() if s !='']
    return [s for s in x.split()]
# 
class pritty_str_arr:
    def __init__(self,data:list[str or float or int]=[],**kwd):
        self.data = data
        self.tap_len = 17
        self.tap_char = " "
        self.include_first_line = False
        self.end_line_char = "$"
        self.max_line_width = 79
        self.after_end_char_string = {}
        self._kwd_process(**kwd)
        self.LINES = []
        self.start_with = ""
        pass
    def __kwdefaults__(self):
        pass
    def _kwd_process(self,**kwd):
        for ky,val in kwd.items():
            if ky in self.__dict__:
                self.__setattr__(ky, val)
        return self
    def process(self,**kwd):
        self._kwd_process(**kwd)
        LINES = []
        
        TMP_STR=self.start_with #if not self.include_first_line else self.start_with+self.tap_char*self.tap_len
        #print(TMP_STR)
        def End_LINE(STR,END_CHAR,MAX_LEN):
            return " "*(MAX_LEN-len(STR))+f"{END_CHAR}"
        for item in self.data:
            #print(item)
            if len(TMP_STR+f"{item} ")>=self.max_line_width:
                LINES+=[TMP_STR+End_LINE(TMP_STR,self.end_line_char,self.max_line_width)]
                TMP_STR=f"{self.tap_char*self.tap_len} {item} "
            else:
                TMP_STR+=f"{item} "
        else:
            if self.tap_len<len(TMP_STR)<self.max_line_width:
                LINES.append(TMP_STR+End_LINE(TMP_STR,self.end_line_char,self.max_line_width))
        # To add comments
        #for i,l in enumerate(LINES):
            #print(f"{i:5}",l,len(l))
        #print(LINES)
        return LINES
        
        
    
def print_fortran(A=[str(x) for x in range(200)],tab=10,full_width=80,include_1st_line=False):
    pass
            


if __name__=="__main__":
    print(str2num(["1","2a"],int).convert(0))
    A = pritty_str_arr(data=[f"{x:05}" for x in range(500)]).process()
    
    