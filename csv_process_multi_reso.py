# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:11:20 2021

@author: yliu
"""

import numpy as np

import pandas as pd

import sys, getopt, os, math

def main(argv):
    width = 1920
    height = 1080
    num_f = 1
    path = '.'
    mr = 1
    ctu_size = 128
    try:
        opts, args = getopt.getopt(argv,"w:h:f:p:m:", ["ctu_size="])
    except getopt.GetoptError:
        print ('csv_process_multi_reso.py -w <width_frame> -h <height_frame> -f <number_frame> -p <path_csv_files> -m <scale_multi_reso> --ctu_size <ctu size>')
        sys.exit(2)
    for opt, arg in opts:      
        if opt == "-w":
            width = int(arg)
        elif opt == "-h":
            height = int(arg)
        elif opt == '-f':
            num_f = int(arg)
        elif opt == '-p':
            path = arg
        elif opt == '-m':
            mr = int(arg)            
        elif opt == '--ctu_size':
            ctu_size = int(arg)
            

    bord_w = int(width/ctu_size)*ctu_size
    bord_h = int(height/ctu_size)*ctu_size

    size_mr = ctu_size/mr
    bord_w_mr = int(width/size_mr)*size_mr
    bord_h_mr = int(height/size_mr)*size_mr

    dim_w_mr = int(width/size_mr)
    dim_h_mr = int(height/size_mr)    

    forbidden_sp_lvl1 = []
    forbidden_sp_lvl2 = []
    
    shift_bits = int(5 * math.log2(mr))
    
    mask_lvl1 = (1 << 5) - 1
    mask_lvl2 = (1 << 10) - 1

    if mr == 2:
        forbidden_sp_lvl2 = [65, 97, 129, 161]

    if mr == 4:
        forbidden_sp_lvl1 = [2, 3, 4, 5]
        forbidden_sp_lvl2 = [65, 97, 129, 161]


    list_files_trace = []

    for dirpath, dirnames, filenames in sorted(os.walk(path)):
        for filename in [f for f in filenames if (f.startswith("mr_" + str(mr)) and str(width) in f and str(height) in f)]:            
            list_files_trace.append(os.path.join(dirpath, filename))

    for f in list_files_trace:
           
        filename = f.split(os.sep)[-1].split('.')[0]
    
        print("Treating multi-reso map of seq {}....".format(filename))
    
        size_mt_mr = int(size_mr / 4)             
        
        split_map = np.empty((num_f, dim_h_mr, dim_w_mr, 1, size_mt_mr, size_mt_mr), dtype=np.int32)
    
        split_map.fill(6)
        
        trace =  pd.read_csv(f, delimiter=';', header = None, keep_default_na=False).to_numpy()

        s_val = []
        s_val_volation = []

        for r in trace: 
            
            if r[1] >= bord_w or r[2] >= bord_h:
                continue
            
            ind_poc = int(r[0])
            
            if mr > 1:
                
                if r[1] >= bord_w_mr or r[2] >= bord_h_mr:
                    continue
                
                
                ind_h_mr = int(r[2] / size_mr)
                ind_w_mr = int(r[1] / size_mr)                     

                ref_x_mt_mr = int((r[1] % size_mr) / 4)
                ref_y_mt_mr = int((r[2] % size_mr) / 4)   

                if (r[1] + r[3]) % size_mr == 0:
                    dx_mt_mr = size_mt_mr - ref_x_mt_mr
                else:    
                    dx_mt_mr = int(((r[1] + r[3]) % size_mr) / 4) - ref_x_mt_mr
                    
                if (r[2] + r[4]) % size_mr == 0:   
                    dy_mt_mr = size_mt_mr - ref_y_mt_mr
    
                else:
                    dy_mt_mr = int(((r[2] + r[4]) % size_mr) / 4) - ref_y_mt_mr


                for i in range(dx_mt_mr):
                    for j in range(dy_mt_mr):

                        assert (split_map[ind_poc, ind_h_mr, ind_w_mr, 0, ref_y_mt_mr + j, ref_x_mt_mr + i] == 6), "The splitserie is not coherent"
    
                        split_map[ind_poc, ind_h_mr, ind_w_mr, 0, ref_y_mt_mr + j, ref_x_mt_mr + i] = r[5] 
                        
                        if r[5] not in s_val:
                            s_val.append(r[5])


        for sp in s_val:

            for sp_w in forbidden_sp_lvl1:
                if ((sp >> shift_bits) & mask_lvl1) == sp_w:
                    s_val_volation.append(sp)
            for sp_w in forbidden_sp_lvl2:
                if ((sp >> shift_bits) & mask_lvl2) == sp_w:
                    s_val_volation.append(sp)

        for sp_w in s_val_volation:
            split_map[split_map == sp_w] = 8
        
        split_map = split_map.reshape(-1, size_mt_mr * size_mt_mr)
        np.savetxt(os.path.join(path, 'Mr_part_' + filename + '.csv'), split_map, fmt='%d', delimiter=';')
            
        

if __name__ == "__main__":
   main(sys.argv[1:])










