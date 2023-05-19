# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:11:20 2021

@author: yliu
"""

import numpy as np

import pandas as pd

import sys, getopt, os

def main(argv):
    width = 1920
    height = 1080
    num_f = 1
    path = '.'
    ctu_size = 128
    try:
        opts, args = getopt.getopt(argv,"w:h:f:p:", ["ctu_size="])
    except getopt.GetoptError:
        print ('csv_process.py -w <width_frame> -h <height_frame> -f <number_frame> -p <path_csv_files> --ctu_size <ctu size>')
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
        elif opt == '--ctu_size':
            ctu_size = int(arg)
            



    bord_w = int(width/ctu_size)*ctu_size
    bord_h = int(height/ctu_size)*ctu_size

    dim_w = int(width/ctu_size)
    
    dim_h = int(height/ctu_size)
    

    list_files_trace = []

    for dirpath, dirnames, filenames in sorted(os.walk(path)):
        for filename in [f for f in filenames if f.startswith("trace_")]:
            list_files_trace.append(os.path.join(dirpath, filename))

    print (list_files_trace)

    for f in list_files_trace:
        
    
        
        # ind_global_ctu = 0
    
        filename = f.split(os.sep)[-1].split('.')[0]
    
        print("treating maps of seq {}....".format(filename))
    
        # ctu = np.empty((size_npy, 128, 128, 1), dtype=np.float16)
        
        # ctu.fill(-1)
    
        size_qt = int(ctu_size / 16)
        size_mt = int(ctu_size / 4)
        
        
        qt_map = np.empty((num_f, dim_h, dim_w, 1, size_qt, size_qt), dtype=np.int8)
    
        qt_map.fill(-1)
    
        mtdepth_map = np.empty((num_f, dim_h, dim_w, 1, size_mt, size_mt), dtype=np.int8)
    
        mtdepth_map.fill(-1)
    
        btdepth_map = np.empty((num_f, dim_h, dim_w, 1, size_mt, size_mt), dtype=np.int8)
    
        btdepth_map.fill(-1)
    
        cushape_map = np.empty((num_f, dim_h, dim_w, 2, size_mt, size_mt), dtype=np.int16)
    
        cushape_map.fill(-1)
    
        
        print(os.path.join(os.path.dirname(filename), 'qt_map_{}.npy'.format(filename)))        
        
        trace =  pd.read_csv(f, delimiter=';', header = None, keep_default_na=False).to_numpy()


        for r in trace: 
            
            if r[1] >= bord_w or r[2] >= bord_h:
                continue
            
            ind_h = int(r[2] / ctu_size)
            ind_w = int(r[1] / ctu_size)
            
            ind_poc = int(r[0])
            
            ref_x_qt = int((r[1] % ctu_size) / 16)
            ref_y_qt = int((r[2] % ctu_size) / 16)

            ref_x_mt = int((r[1] % ctu_size) / 4)
            ref_y_mt = int((r[2] % ctu_size) / 4)
            

            if (r[1] + r[3]) % ctu_size == 0:
                dx_qt = size_qt - ref_x_qt
                dx_mt = size_mt - ref_x_mt
            else:    
                dx_mt = int(((r[1] + r[3]) % ctu_size) / 4) - ref_x_mt
                dx_qt = int(((r[1] + r[3] + 12) % ctu_size) / 16) - ref_x_qt
                
            if (r[2] + r[4]) % ctu_size == 0:   
                dy_qt = size_qt - ref_y_qt
                dy_mt = size_mt - ref_y_mt

            else:
                dy_qt = int(((r[2] + r[4] + 12) % ctu_size) / 16) - ref_y_qt
                dy_mt = int(((r[2] + r[4]) % ctu_size) / 4) - ref_y_mt


            for i in range(dx_qt):
                for j in range(dy_qt):
                    assert (qt_map[ind_poc, ind_h, ind_w, :, ref_y_qt + j, ref_x_qt + i] == -1 or qt_map[ind_poc, ind_h, ind_w, :, ref_y_qt + j, ref_x_qt + i] == r[7]), "The qt size is not coherent"
                    qt_map[ind_poc, ind_h, ind_w, :, ref_y_qt + j, ref_x_qt + i] = r[7] 
            
            
            for i in range(dx_mt):
                for j in range(dy_mt):


                    assert (mtdepth_map[ind_poc, ind_h, ind_w, :, ref_y_mt + j, ref_x_mt + i] == -1), "The mtdepth is not coherent"
                    assert (btdepth_map[ind_poc, ind_h, ind_w, :, ref_y_mt + j, ref_x_mt + i] == -1), "The btdepth is not coherent"
                    
                    assert (cushape_map[ind_poc, ind_h, ind_w, 0, ref_y_mt + j, ref_x_mt + i] == -1), "The cushape is not coherent"

                    mtdepth_map[ind_poc, ind_h, ind_w, :, ref_y_mt + j, ref_x_mt + i] = r[8] 
                    btdepth_map[ind_poc, ind_h, ind_w, :, ref_y_mt + j, ref_x_mt + i] = r[9]
                    cushape_map[ind_poc, ind_h, ind_w, 0, ref_y_mt + j, ref_x_mt + i] = r[3] 
                    cushape_map[ind_poc, ind_h, ind_w, 1, ref_y_mt + j, ref_x_mt + i] = r[4]
                    


        np.save( os.path.join(os.path.dirname(f), 'qt_map_{}.npy'.format(filename)), qt_map)
    
        np.save( os.path.join(os.path.dirname(f), 'mtdepth_map_{}.npy'.format(filename)), mtdepth_map)
    
        np.save( os.path.join(os.path.dirname(f), 'btdepth_map_{}.npy'.format(filename)), btdepth_map)    
        
        np.save( os.path.join(os.path.dirname(f), 'cushape_map_{}.npy'.format(filename)), cushape_map)        
        

    
    
        if -1 in qt_map:
            raise Exception('-1 value is in QTdepth map')
    
        if -1 in mtdepth_map:
            raise Exception('-1 value is in mtdepth map')
    
        if -1 in btdepth_map:
            raise Exception('-1 value is in btdepth map')
    
        if -1 in cushape_map:
            raise Exception('-1 value is in cushape map')



if __name__ == "__main__":
   main(sys.argv[1:])










