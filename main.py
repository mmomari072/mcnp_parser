# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:29:08 2024

@author: mohammed.omari
"""
# from cellcard import cell_card
# from auxfuntions import *
from input_file import input_file


if __name__=="__main__":
    import sys
    if sys.platform.find("win")>=0:
        fname = r"G:\DATA_FUJITSU\Users\Mohammed\Desktop\Old & ongoing\JRTR_MCNP\JRTR_RPT_FullCore_InitialCore_for_JAEC-308K-MCNP_FOR_TESTING.DAT"
    else:
        fname = "../JRTR_RPT_FullCore_InitialCore_for_JAEC-308K-MCNP.DAT"
    I = input_file()
    I.import_file(fname)
    I.find_blocks_index()
    I.parsing_file_blocks()
    
    for i,cell in I.cell_card.cells.items():
        if cell.options.u.value is not None:
            #print(i,cell.options.u.value)
            pass
            
    txt = """3654 2 -2.699 (-204:205:-116:117:-211:212)
              203 -206  115  -118  213 -214  u=114  imp:n=1"""
    from time import sleep
    #print(txt.split("\n"))
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
                
    CELL_IDs = I.cell_card.look_for(u=102)
    index = I.cell_card.look_for(fill=102)

    FUEL_ASSEMBLEY = I.cell_card[index+CELL_IDs]
    with open(r"G:\DATA_FUJITSU\Users\Mohammed\Documents\New folder (2)\MCNP_FUEL_ASSEMBLE_OMARI_EXTRACTED.DAT","w") as fid:
        print(I.title,file=fid)
        
        for cell in FUEL_ASSEMBLEY:
            #cell.options.u.value=None
            #cell.material_id=0
            #cell.material_density =None
            for line in cell.export_mcnp():
                print(line,file=fid)
        print(f"0    0   #{index[0]} imp:n=0",file=fid)
        print(file=fid)
        for block in [I.surface_card,I.options_card]:
            for line in block.raw_data:
                print(line,file=fid)
            print(file=fid)


        