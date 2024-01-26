# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:29:08 2024

@author: mohammed.omari
"""
from cellcard import cell_card
from auxfuntions import *

class input_file:
    def __init__(self):
        self.filename = None
        self.raw_txt = []
        self.name=None
        self.title = title()
        self.cell_card = cell_card()
        self.surface_card = surface_card()
        self.maerial_card = []
        self.options_card = options_card()
        self.blocks_index = dict(
            title=[0,1],
            cell_card=[None,None],
            surface_card=[None,None],
            options_card=[None,None])
    
    def import_file(self,filename=None):
        if filename is not None:
            self.filename = filename
        with open(self.filename,"r") as fid:
            self.raw_txt = [l.strip("\n") for l in fid]
        return self
    
    def find_blocks_index(self):
        INDEX=[0,]
        for i,txt in enumerate(self.raw_txt):
            if i==0:
                continue
            if txt.strip()=='':
                INDEX.append(i)
                
        print(INDEX)
        #MAP = {0:"title",1:"cell_card",2:"surface_card",3:"options_card"}
        for i,index in enumerate(INDEX[1:]):
            #self.blocks_index[MAP[i]]=[index,]
            pass
        self.blocks_index["cell_card"]    = [1,INDEX[1]-1]
        self.blocks_index["surface_card"] = [INDEX[1]+1,INDEX[2]-1]
        self.blocks_index["options_card"] = [INDEX[2]+1,len(self.raw_txt)]
        print(self.blocks_index)
        return self
    
    def parsing_file_blocks(self):
        #self.title = self.raw_txt[self.blocks_index["title"][0]]
        for ky,Range in self.blocks_index.items():
            print(ky,Range)
            tmp_line = self.raw_txt[slice(*self.blocks_index[ky])]
            self.__dict__[ky].parse(tmp_line)
        return self
            
class title:
    def __init__(self):
        self.raw_data = []
        self.value = None
    def parse(self,lines:list[str]):
        self.raw_data = lines
        self.value = lines[0]
        
# ######################################################################
class surface_card:
    def __init__(self):
        self.raw_data = []
        self.value = None
    def parse(self,lines):
        self.raw_data = lines
        #self.value = lines[0]
    
class options_card:
    def __init__(self):
        self.raw_data = []
        self.value = None
    def parse(self,lines=[str]):
        self.raw_data = lines
       

if __name__=="__main__":
    fname = r"G:\DATA_FUJITSU\Users\Mohammed\Desktop\Old & ongoing\JRTR_MCNP\JRTR_RPT_FullCore_InitialCore_for_JAEC-308K-MCNP.DAT"
    I = input_file()
    I.import_file(fname)
    I.find_blocks_index()
    I.parsing_file_blocks()
    
    for i,cell in I.cell_card.cells.items():
        if cell.options.u.value is not None:
            print(i,cell.options.u.value)
            
    txt = """3654 2 -2.699 (-204:205:-116:117:-211:212)
              203 -206  115  -118  213 -214  u=114  imp:n=1"""
    from time import sleep
    print(txt.split("\n"))
    for line in I.cell_card.raw_data:
        #print(line)
        #sleep(0.01)
        pass
    
    U=[]
    for c,cell in I.cell_card.cells.items():
        if cell.options.u.value not in U:
            U.append(cell.options.u.value)
    
    MAT_ID ={}
    for c,cell in I.cell_card.cells.items():
        if cell.material_id not in MAT_ID:
            MAT_ID[cell.material_id]=[cell.material_density] 
        else:
            if cell.material_density not in MAT_ID[cell.material_id]:
                MAT_ID[cell.material_id]+=[cell.material_density]
            

        