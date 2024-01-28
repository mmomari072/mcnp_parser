# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:54:33 2024

@author: mohammed.omari
"""
from auxfuntions import *
class cell_card:
    def __init__(self):
        self.raw_data=[]
        self.cells={}
        self.cells_indexs_in_raw_data=[]
        #self.cells_indexs_in_raw_data2=[]
        
        self.__look_for_index = []
        pass
    def parse(self, lines:list[str]):
        self.raw_data = lines
        print("parsing cell card")
        
        # Searching for cells
        for i,line in enumerate(self.raw_data):
            tmp=line.split() #Split_txt(line,False)
            #print(tmp)
            if str2num(tmp[0],int).IsType() and line.find("    ")!=0:
                self.cells_indexs_in_raw_data.append(i)

        self.cells_indexs_in_raw_data.append(len(self.raw_data))
        #
        for i in range(len(self.cells_indexs_in_raw_data)-1):
            # Cell Start and End Lines
            start,end = self.cells_indexs_in_raw_data[i],self.cells_indexs_in_raw_data[i+1]
            # Return the related string list
            tmp_txt = self.raw_data[slice(start,end)]
            # Processing the 
            #print(tmp_txt)
            tmp_cell = cell().parse(tmp_txt)
            self.cells[tmp_cell.id]=tmp_cell
        return self
    
    def look_for(self,paramters={},**kwd):
        INDEX=[]
        for c_id,cell in self.cells.items():
            STAT = []
            for Case in [paramters,kwd]:
                for ky,val in Case.items():
                    if sum([ky.find(x)>=0 for x in cell_options().__keys__]):# ky in cell_options().__keys__:
                        #print(ky,val)
                        STAT.append(cell.options.has_value({ky:val}))
                    elif ky.lower() in ["mat_id","material_id"]:
                        STAT.append(cell.material_id==val)
                    elif ky.lower() in ["rho","material_density","density"]  :
                        STAT.append(cell.material_density==val)
                    elif ky.lower() in ["surface","surf"]:
                        print("Search for surface has not been developed yet!")
                    elif ky.lower() in ["cell"]:
                        print("Search for cell has not been developed yet!")
                    else:
                        Warning(f" [{ky}] paramter is not supported!")
                        
            if all(STAT):
                INDEX.append(c_id)
        self.__look_for_index=INDEX 
        return INDEX
    
    def __getitem__(self,index):
        if isinstance(index, (list,tuple,set)):
            return [self[i] for i in index]
        elif isinstance(index, int):
            return self.cells[index]
        elif isinstance(index, slice):
            I=list(range(len(self.cells)))
            return self[I[index]]
        else:
            Warning(f"[{type(index)}][index] is not supported!")
            return 
    def __repr__(self):
        return "Not Yet Cell Card"
            
            

class _general_option:
    def __init__(self):
        self.value = None
        self.key = None
        self.raw_data = []
    def parse(self,opt,vals):
        if opt!=self.key:
            Warning(f"Wrong mcnp option {opt} <--> {self.key}")
        #tmp=opt.split("=")
        self.raw_data = vals
        conveter = float
        if self.key in ["u","lat"]:
            conveter=int
            self.value = str2num(vals,conveter).convert()[0]
        elif self.key in ["vol","tmp"]:
            self.value = str2num(vals,conveter).convert()[0]
            pass
        elif self.key is None:
            pass
        else:
            print(f"{self.key} cell card option has not been developed yet!")
        return self.check()
    def check(self):
        return self
    def __str__(self):
        if self.value is not None:
            return f"{self.key}={self.value}".upper()
        return ""
    
    #@property
    def __call__(self):
        return self.value
    
    def __repr__(self):
        return str(self)
    def has_value(self,*arg):
        if len(arg)==2:
            if arg[0].find(self.key)<0:
                return False
            return arg[1]==self.value
        elif len(arg)==1:
            return arg[0]==self.value
        return False

            
class _universe(_general_option):
    def __init__(self):
        super().__init__()
        self.key="u"
    def check(self):
        return isinstance(self.value, int)
    
class _importance:
    _particles = dict(n="neutron",
                      p="photon",
                      e="electron",
                      h="hydron")
    def __init__(self):
        super().__init__()
        self.key="imp"
    def parse(self,opt,val):
        #print(opt)
        particles = opt.lower().split("imp:")[1].split(",")
        #print(particles)
        if len(val)!=1:
            Warning("Warning in Importance option")
        for p in particles:
            if str2num(val[0],int).IsType():
                self.__dict__[p]=str2num(val[0],int).convert()
            elif str2num(val[0],float).IsType():
                self.__dict__[p]=str2num(val[0],float).convert()
            else:
                self.__dict__[p]=val[0]
        self.check()
        return self
    def check(self):
        return all([isinstance(v, (int,float)) for v in 
                    [val for a,val in self.__dict__.items() if a in self._particles
            ]])
    
    def has_value(self,*arg):
        if len(arg)==1:
            return all([x==val for x in [xx for p,xx in self.__dict__.items() if p in self._particles]])
        if len(arg)==2:
            particles = arg[0].lower().split("imp:")[1].split(",")
            STAT=[]
            for p in particles:
                if p not in self.__dict__ or p not in self._particles:
                    return False
                STAT.append(self.__dict__[p] ==arg[1])
            return all(STAT)
        else:
            return False
        
    def __str__(self):
        STR=""
        for p in self._particles:
            if p in self.__dict__:
                STR+=f"imp:{p}={self.__getattribute__(p)} ".upper()
        return STR .strip()
                
                    

class _volume(_general_option):
    def __init__(self):
        super().__init__()
        self.key="vol"
    pass

class _temperature(_general_option):
    def __init__(self):
        super().__init__()
        self.key="tmp"
    def convert_to_K(self):
        k=1
        return self.value*k

class _latice(_general_option):
    def __init__(self):
        super().__init__()
        self.key="lat"
    def check(self):
        if self.value in [1,2]:
            return True
        return False

class _fill(_general_option):
    def __init__(self):
        super().__init__()
        self.key="fill"
    def parse(self,opt,val):
        self.raw_data = val
        if len(val)==1:
            self.value = str2num(val,int).convert()[0]
        else:
            Warning("Fill matrix has not been supported yet")
        return self
    def check(self):
        Warning("Check Fill has not been developed yet!")
        return True
    
    

class _translation(_general_option):
    pass

    
cell_option_keys = dict(u=_universe(),
                imp=_importance(),
                vol=_volume(),
                tmp=_temperature(),
                lat=_latice(),
                fill=_fill(),
                tcl=_translation(),
                trcl=_translation())


class cell:
    def __init__(self):
        self.raw_data = []
        self.name = None
        self.id = None
        self.material_id = None
        self.material_density = None
        self.geometry = cell_geomtery()
        self.GEOM = []
        self.options = cell_options()
        self.d_comments = []
        self.c_commments=[]
        
    def parse(self,data):
        self.raw_data = data
        FULL_STR=""
        # Get the comments and remove them from the actual cell defintion
        for line in self.raw_data:
            if line.lower().find("c")==0:
                self.c_commments.append(line)
                continue
            d_sign_index = line.find("$")
            if d_sign_index>=0:
                self.d_comments.append(line[d_sign_index:])
                FULL_STR+=line[:d_sign_index]
            else:
                FULL_STR+=line
        
        # REMOVE DOUBLE BLANK
        while (FULL_STR.find("  ")>=0):
            FULL_STR = FULL_STR.replace("  "," ")
            pass
                    
        # Adjust some blanks
        for char,val in {"&":" ", "=":"= "}.items():
            FULL_STR = FULL_STR.replace(char,val).lower()
        
        # Start Processing the string
        tmp=Split_txt(FULL_STR)
        # print("FULL:",FULL_STR)
        # print(tmp)
        
        # Get Cell ID
        self.id = str2num(tmp[0],int).convert()
        if FULL_STR.find("like")>=0:
            print("LIKE BUT is not supported!, to be developed later")
            return self
            pass
        # Get Material information
        self.material_id = str2num(tmp[1],int).convert()
    
        ## search for geomtery information
        cell_i_start = 2
        if self.material_id>0:
            self.material_density=str2num(tmp[2],float).convert()
            cell_i_start = 3
        cell_i_end = len(tmp)-1
        for i in range(cell_i_start,len(tmp)):
            do_break=False
            for k in cell_option_keys.keys():
                if tmp[i].find(k)>=0:
                    #print(tmp,tmp[i])
                    cell_i_end = i-1
                    do_break = True
                    break
            if do_break:
                break
        # Process Geometry information
        self.GEOM = tmp[cell_i_start:cell_i_end+1]
        self.geometry.parse(self.GEOM)
        # Process options
        self.options.parse(tmp[cell_i_end+1:])
        
        return self
    
    def __repr__(self):
        return f"""
    ID       : {self.id}
    Mat ID   : {self.material_id}
    RHO      : {self.material_density}
    OPTIONS  : {str(self.options)}
    """
    
    def export_mcnp(self):
        rho = f"{self.material_density:10.8g}" if self.material_id>0 else " "*10
        first_words =f"{self.id:<5}  {self.material_id:<5} {rho} "
        
        LINES=pritty_str_arr(
                   data=[first_words]+self.geometry.geo,tap_len=len(first_words),
                   ).process()
        #print(pritty_str_arr(data=[" "*len(first_words)]+self.options.export_mcnp())).process()
        return LINES+pritty_str_arr(data=[" "*len(first_words)]+self.options.export_mcnp()).process()
        
        
        
        

class cell_geomtery:
    def __init__(self):
        self.full_text = ""
        self.raw_data=[]
        self.geo = []
    def parse(self,str_list:list[str]):
        self.raw_data = str_list
        def process_array(arr):
            B=[]
            
            for item in arr:
                for char in [":","(",")"]:
                    item=item.replace(char,f" {char} ")
                B+=[x for x in item.split() if x!='']
            #print("This is B in process_array subfun",B)
            return B
        ITEMS=process_array(self.raw_data)

        A=[]
        for i,item in enumerate(ITEMS):
            if item.find(":")==0:
                A.append(OR())
                continue
            if item.find("#")>=0 and len(item)>1:
                if isinstance(A[-1], OR):
                    A+=[COMPLEMENT(item[1:])]
                elif ~isinstance(A[-1], AND):
                    A+=[AND(),COMPLEMENT(item[1:])]
                else:
                    Warning("CHECK THIS ONE!!")
                continue
            elif item.find("#")>=0:
                Warning("CHECK # COMPLEMENT")
            if i==0 or i==(len(ITEMS)-0):
                A.append(item)
                if i==(len(ITEMS)-1):
                    break
                continue
            if isinstance(A[-1],(OR,)) or A[-1] in ["(",] or item in [")"]:
                A.append(item)
            # elif (i<len(ITEMS)-1 or True) and (ITEMS[i] in [")"]):
            #     #print("BINGOOOOOOO",item,ITEMS[i+1])
            #     A.append(item)
            else:
                A+=[AND(),item]
            
            #print(A)
            
        self.geo=A
        return self
    
    def __repr__(self):
        STR=""
        for l in pritty_str_arr(data=self.geo).process(include_first_line=True):
            STR+=f"{l}\n"
        
        return STR
    
class _Bool_Operator:
    def __init__(self):
        self.str_char = " "
        self.repr_char = " BOOL_OPERATOR "
    def __repr__(self):
        return self.repr_char
    def __str__(self):
        return self.str_char

class AND(_Bool_Operator):
    def __init__(self):
        super().__init__()
        self.str_char = " "
        self.repr_char = "-AND-"
        pass
    
class OR(_Bool_Operator):
    def __init__(self):
        self.str_char = ":"
        self.repr_char = "-OR-"
        pass
    
class COMPLEMENT(_Bool_Operator):
    def __init__(self,cell_id):
        self.str_char = "#"
        self.repr_char = "-COMPLEMENT-"
        self.cell_id = cell_id
        pass
    def __repr__(self):
        return self.repr_char+f"{self.cell_id}"
    def __str__(self):
        return self.str_char+f"{self.cell_id}"
    

    

from copy import deepcopy
class cell_options:
    # *************************************************************************
    def _search_in(self,item,list_items):
        """
        This function is used to check if an string my have char(s) in list
        """
        for i in list_items:
            if item.find(i)>=0:
                return i
        return 
    
    
    __keys__ = cell_option_keys
    # *************************************************************************
    def __init__(self):
        for k,val in self.__keys__.items():
            self.__dict__[k]=deepcopy(val)
        self.raw_data = []
        pass
    
    def parse(self,str_arr=[str]):
        search_in =self._search_in
        def fix_array(x:list[str]):
            A=[]
            for xx in x:
                if xx.find("=")>=0:
                    for xxx in xx.split("="):
                        if xxx!="":
                            A.append(xxx.strip())
                    continue
                A.append(xx.strip())
            return A

        self.raw_data = str_arr
        KEYS=list(self.__keys__.keys())        
        opt_array = fix_array(self.raw_data)
        indexes= {}
        #
        for i,item in enumerate(opt_array):
            ky = search_in(item,KEYS)
            if ky is None:
                continue
            indexes[item]=[]
            for j,item2 in enumerate(opt_array[i:]):
                if item2.find(ky)>=0:
                    continue
                tmp_k=search_in(item2,KEYS)
                if tmp_k is None:
                    indexes[item].append(item2)
                else:
                    break
        
        for opt,vals in indexes.items():
            #print("BINGO",opt,vals)
            tmp_opt=search_in(opt, KEYS)
            self.__dict__[tmp_opt].parse(opt,vals)
        
        return self
    
    def has_value(self,paramters={},**kwd):
        STAT=[]
        for case in [paramters,kwd]:
            for ky,val in case.items():
                act_ky=self._search_in(ky.lower(), self.__keys__.keys())
                STAT+=[self.__dict__[act_ky].has_value(ky.lower(),val)]
        return all(STAT)
    
    def export_mcnp(self):
        return [str(val) for k,val in self.__dict__.items() if (k in self.__keys__  and str(val)!='')]
    
    def __str__(self):
        return "cell options representation has not been developed yet"


if __name__=="__main__":

    GG = ['(-204:205:-168:169:-211:212)', '203', '-206', '167', '-170', '213', '-214']
#    process_array(GG)

    cells = cell()
    cells.geometry.parse(['201', '-208', '101', '-188', '325',":","1", '#-326'])
    cells.geometry.parse(
        ['(-204:205:-168:169:-211:212)', '203', '-206', '167', '-170', '213', '-214']
        )
    copt = cell_options()
    copt.parse(str_arr= ['u =', '101', "fill","2",'imp:n,p=1', '1','vol=',"2","lat","44","imp:e=","1"])
