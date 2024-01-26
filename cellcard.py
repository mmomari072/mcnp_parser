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
            print(tmp_txt)
            tmp_cell = cell().parse(tmp_txt)
            self.cells[tmp_cell.id]=tmp_cell
        return self
    
    def search_for(self,**kwd):
        INDEX=[]
        for c_id,cell in self.cells.items():
            case = []
            for ky,val in kwd.items():
                if ky in cell_options().__keys__:
                    if cell.options.__dict__[ky].value==val:
                        case.append(True)
                    else:
                        case.append(False)
                elif ky.lower() in ["mat_id","material_id"]:
                    case.append(cell.material_id==val)
                elif ky.lower() in ["rho","material_density","density"]  :
                    case.append(cell.material_density==val)
            if all(case):
                INDEX.append(c_id)
        return INDEX

            
            

class _general_option:
    def __init__(self):
        self.value = None
        self.key = None
    def parse(self,opt):
        tmp=opt.split("=")
        conveter = float
        if self.key in ["u","lat","fill"]:
            conveter=int
        self.value = str2num(tmp[1],conveter).convert()
        pass
    def __str__(self):
        if self.value is not None:
            return f"{self.key}={self.value}".upper()
        return ""
    pass

class _universe(_general_option):
    def __init__(self):
        super().__init__()
        self.key="u"

    
class _importance:
    def parse(self,opt):
        pass

class _volume(_general_option):
    def __init__(self):
        super().__init__()
        self.key="vol"
    pass

class _temperature(_general_option):
    def __init__(self):
        super().__init__()
        self.key="tmp"

class _latice(_general_option):
    def __init__(self):
        super().__init__()
        self.key="lat"

class _fill(_general_option):
    def __init__(self):
        super().__init__()
        self.key="fill"

class _translation:
    def parse(self,opt):
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
        self.geomatery = None
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
        # for char,_ in cell_option_keys.items():
        #     if FULL_STR.find(char)>=0 and char!="imp":
        #         if FULL_STR.find(f"{char}=")<0:
        #             FULL_STR=FULL_STR.replace(char,f"{char}=")                    
        #             print("Bingo",FULL_STR)
        #             #exit()
        #     elif FULL_STR.find(char)>=0 and char!="imp":
                
                

                    
        # Adjust some blanks
        for char,val in {"&":" ", "=":"= "}.items():
            FULL_STR = FULL_STR.replace(char,val).lower()
        

        
        # Start Processing the string
        tmp=Split_txt(FULL_STR)
        print("FULL:",FULL_STR)
        print(tmp)
        
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
        
        # Process options
        self.options.parse(tmp[cell_i_end+1:])
        
        return self

        
        
        

class cell_geomtery:
    def __init__(self):
        self.full_text = ""
    
from copy import deepcopy
class cell_options:
    __keys__ = cell_option_keys
    def __init__(self):
        for k,val in self.__keys__.items():
            self.__dict__[k]=deepcopy(val)
        self.raw_data = []
    def parse(self,str_arr=[str]):
        self.raw_data = str_arr
        #print(self.raw_data)
        #self.value = lines[0]
        indexes = {}
        KEYS=list(self.__keys__.keys())
        
        
        KK = {}
        
        for ky1 in KEYS:
            KK[ky1]=[]
            for i,item in enumerate(self.raw_data):
                if item.find(ky1)>=0:
                    for j,item2 in enumerate(self.raw_data[i+1:]):
                        STOP=False
                        for ky2 in KEYS:
                            if ky1==ky2:
                                print("Musebah")
                                continue
                            if item2.find(ky2)>=0:
                                STOP=True
                            if STOP:
                                break
                            
                        if STOP:
                            STOP
                        KK[ky1].append(j+i+1)
        print(KK)
        while j<len(self.raw_data):
            txt = self.raw_data[j]
            for ky in KEYS:
                if ky in KK:
                    print("SHI",k,ky)
                    continue
                if txt.find(ky)>=0:
                    KK[ky]=[j+1]
                    j+=1
                    while j<len(self.raw_data):
                        txt2 = self.raw_data[j]
                        for ky2 in KEYS:
                            if txt2.find(ky2)>=0:
                                print("SH2",j)
                                break
                        KK[ky].append(j+1)
                        j+=1
            j+=1
            print(KK)
        
        
        for i,ky in enumerate(KEYS):
            j=0
            #print(i,ky)
            start = None
            end   = None
            KEYS_min_ky = [k for k in KEYS if k!=ky]
            while j<len(self.raw_data):
                txt=self.raw_data[j]
                if txt.find(ky)>=0:
                    start=j+1 
                j+=1
                for ky2 in KEYS_min_ky:
                    while j<len(self.raw_data):
                        txt=self.raw_data[j]
                        if txt.find(ky2)>=0:
                            end = j
                            break
                        j+=1
                    if end is not None:
                        break
            
            if all([x is not None for x in [start,end]]):
                print(ky,"START<END:",start,end)
                    
                        
            # for j,val in enumerate(self.raw_data):
            #     if val.find(ky)>=0:
            #         print("bingo1")
            #         start = j+1
            #         end = start+1
            #         for k,val2 in enumerate(self.raw_data[j+1:]):
            #             breakthis = False
            #             for l,ky2 in enumerate(KEYS):
            #                 if l==i:
            #                     print("Bingo: CONTINUE!")
            #                     continue
            #                 if val2.find(ky2)>=0:
            #                     print("START,END",start,k,ky,ky2)
            #                     end=k
            #                     breakthis = True
            #                     break
            #             if breakthis:
            #                 break
            # if start is not None and end is not None:
            #     print(start,end)
                        
                
                
        # while i<len(self.raw_data):
        #     word=self.raw_data[i]
        #     start=i
        #     for ky in KEYS:
        #         if work.find(ky)>=0:
        #             start=i+1
        #             end=i+1
        #             i+=1
        #             while True:
        #                 for ky2 in KEYS:
        #                     if self.raw_data[i].find(ky2)>=0:
        # #                         end=i
        # #                         break
                        
        #         pass
        #     i+=1
        #     pass
        for i,opt in enumerate(self.raw_data):
            indexes[opt.replace("=","").strip()]=[i,None]
            start_=False
            for ky in self.__keys__:
                if opt.find(ky)>=0:
                    print(i,ky,opt)
                    self.__dict__[ky].parse(opt)
            pass
        
        return self


if __name__=="__main__":
    copt = cell_options()
    copt.parse(str_arr= ['u=', '101', 'imp:n=', '1'])
