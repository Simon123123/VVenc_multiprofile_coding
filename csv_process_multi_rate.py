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
        opts, args = getopt.getopt(argv,"w:h:f:p:m:", ["ctu_size="])
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
        for filename in [f for f in filenames if (f.startswith("trace_") and str(width) in f and str(height) in f)]:           
            list_files_trace.append(os.path.join(dirpath, filename))


    for f in list_files_trace:
        
    
        filename = f.split(os.sep)[-1].split('.')[0]
    
        print("Treating multi-rate map of seq {}....".format(filename))
    

        size_mt = int(ctu_size / 4)
          
        cushape_map = np.empty((num_f, dim_h, dim_w, 2, size_mt, size_mt), dtype=np.int16)
    
        cushape_map.fill(-1)    
        
        trace =  pd.read_csv(f, delimiter=';', header = None, keep_default_na=False).to_numpy()


        for r in trace: 
            
            if r[1] >= bord_w or r[2] >= bord_h:
                continue
            
            ind_h = int(r[2] / ctu_size)
            ind_w = int(r[1] / ctu_size)
            
            
            ind_poc = int(r[0])
            

            ref_x_mt = int((r[1] % ctu_size) / 4)
            ref_y_mt = int((r[2] % ctu_size) / 4)
            

            if (r[1] + r[3]) % ctu_size == 0:
                dx_mt = size_mt - ref_x_mt
            else:    
                dx_mt = int(((r[1] + r[3]) % ctu_size) / 4) - ref_x_mt
                
            if (r[2] + r[4]) % ctu_size == 0:   
                dy_mt = size_mt - ref_y_mt

            else:
                dy_mt = int(((r[2] + r[4]) % ctu_size) / 4) - ref_y_mt

            
            for i in range(dx_mt):
                for j in range(dy_mt):


                    assert (cushape_map[ind_poc, ind_h, ind_w, 0, ref_y_mt + j, ref_x_mt + i] == -1), "The cushape is not coherent"

                    cushape_map[ind_poc, ind_h, ind_w, 0, ref_y_mt + j, ref_x_mt + i] = r[3] 
                    cushape_map[ind_poc, ind_h, ind_w, 1, ref_y_mt + j, ref_x_mt + i] = r[4]
                    

 
        cushape_map = cushape_map.reshape(-1, size_mt * size_mt)
        np.savetxt(os.path.join(path, 'ShapeMap_' + filename + '.csv'), cushape_map, fmt='%d', delimiter=';')
        

        if -1 in cushape_map:
            raise Exception('-1 value is in cushape map')


if __name__ == "__main__":
   main(sys.argv[1:])










