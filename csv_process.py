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
    try:
        opts, args = getopt.getopt(argv,"w:h:f:p:")
    except getopt.GetoptError:
        print ('csv_process.py -w <width_frame> -h <height_frame> -f <number_frame> -p <path_csv_files>')
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



    bord_w = int(width/128)*128
    bord_h = int(height/128)*128

    size_npy = int(width/128) * int(height/128) * num_f

    # list_files_ctu = []
    list_files_trace = []

    # for dirpath, dirnames, filenames in sorted(os.walk(path)):
    #     for filename in [f for f in filenames if f.startswith("CTU_")]:
    #         list_files_ctu.append(os.path.join(dirpath, filename))

    for dirpath, dirnames, filenames in sorted(os.walk(path)):
        for filename in [f for f in filenames if f.startswith("trace_")]:
            list_files_trace.append(os.path.join(dirpath, filename))



    for f in list_files_trace:
        
        
        ind_global_trace = 0
        
        # ind_global_ctu = 0
    
        filename = f.split(os.sep)[-1].split('.')[0]
    
        print("treating maps of seq {}....".format(filename))
    
        # ctu = np.empty((size_npy, 128, 128, 1), dtype=np.float16)
        
        # ctu.fill(-1)
    
        qt_map = np.empty((size_npy, 8, 8, 1), dtype=np.int8)
    
        qt_map.fill(-1)
    
        mtdepth_map = np.empty((size_npy, 32, 32, 1), dtype=np.int8)
    
        mtdepth_map.fill(-1)
    
        btdepth_map = np.empty((size_npy, 32, 32, 1), dtype=np.int8)
    
        btdepth_map.fill(-1)
    
        cushape_map = np.empty((size_npy, 32, 32, 2), dtype=np.int8)
    
        cushape_map.fill(-1)
    
    
        # mt1_map = np.empty((size_npy, 32, 32, 1), dtype=np.int8)
    
        # mt1_map.fill(-1)
    
        # mt2_map = np.empty((size_npy, 32, 32, 1), dtype=np.int8)
    
        # mt2_map.fill(-1)        
        
        print(os.path.join(os.path.dirname(filename), 'qt_map_{}.npy'.format(filename)))        
        
        trace =  pd.read_csv(f, delimiter=';', header = None, keep_default_na=False).to_numpy()


        for r in trace: 
            
            if r[1] >= bord_w or r[2] >= bord_h:
                continue
            
            
            # mt_dep = int(r[5]) >> int(5*r[6])
                
            # mt1_split = mt_dep & 31
            # mt2_split = (mt_dep >> 5) & 31


            ref_x_qt = int((r[1] % 128) / 16)
            ref_y_qt = int((r[2] % 128) / 16)

            ref_x_mt = int((r[1] % 128) / 4)
            ref_y_mt = int((r[2] % 128) / 4)
            

            if (r[1] + r[3]) % 128 == 0:
                dx_qt = 8 - ref_x_qt
                dx_mt = 32 - ref_x_mt
            else:    
                dx_mt = int(((r[1] + r[3]) % 128) / 4) - ref_x_mt
                dx_qt = int(((r[1] + r[3] + 12) % 128) / 16) - ref_x_qt
                
            if (r[2] + r[4]) % 128 == 0:   
                dy_qt = 8 - ref_y_qt
                dy_mt = 32 - ref_y_mt

            else:
                dy_qt = int(((r[2] + r[4] + 12) % 128) / 16) - ref_y_qt
                dy_mt = int(((r[2] + r[4]) % 128) / 4) - ref_y_mt


            for i in range(dx_qt):
                for j in range(dy_qt):
                    assert (qt_map[ind_global_trace, ref_y_qt + j, ref_x_qt + i, :] == -1 or qt_map[ind_global_trace, ref_y_qt + j, ref_x_qt + i, :] == r[7]), "The qt size is not coherent"
                    qt_map[ind_global_trace, ref_y_qt + j, ref_x_qt + i, :] = r[7] 
            
            
            for i in range(dx_mt):
                for j in range(dy_mt):


                    assert (mtdepth_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] == -1), "The mtdepth is not coherent"
                    assert (btdepth_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] == -1), "The btdepth is not coherent"
                    
                    assert (cushape_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, 0] == -1), "The cushape is not coherent"

                    mtdepth_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] = r[8] 
                    btdepth_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] = r[9]
                    cushape_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, 0] = r[3] 
                    cushape_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, 1] = r[4]
                    


                    # assert (mt1_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] == -1), "The mt1 decision is not coherent"
                    # assert (mt2_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] == -1), "The mt2 decision is not coherent"

                    # mt1_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] = mt1_split
                    # mt2_map[ind_global_trace, ref_y_mt + j, ref_x_mt + i, :] = mt2_split


            if (r[1] + r[3]) % 128 == 0 and (r[2] + r[4]) % 128 == 0:

                ind_global_trace += 1                
                # if (ind_global_trace % int(1e5) == 0):
                #     print("Treating partition maps on line :", ind_global_trace)                
                



    # for f in list_files_ctu:
    
    #     ctu_file = pd.read_csv(f, delimiter=';', header = None, keep_default_na=False).to_numpy()

    #     for r in ctu_file: 
            
    #         assert (ctu[ind_global_ctu, 0, 0, 0] == -1), "The ctu value is not coherent"
    #         ctu[ind_global_ctu, :, :, :] = np.array(r[3:-1].reshape(128, 128, 1)/1024, dtype = np.float16)
            
    #         ind_global_ctu += 1


    # np.save( os.path.join(path, 'ctu.npy'), ctu)

    # np.save( os.path.join(path, 'qt_map.npy'), qt_map)

    # np.save( os.path.join(path, 'mt1_map.npy'), mt1_map)

    # np.save( os.path.join(path, 'mt2_map.npy'), mt2_map)
    
    

        np.save( os.path.join(os.path.dirname(f), 'qt_map_{}.npy'.format(filename)), qt_map)
    
        np.save( os.path.join(os.path.dirname(f), 'mtdepth_map_{}.npy'.format(filename)), mtdepth_map)
    
        np.save( os.path.join(os.path.dirname(f), 'btdepth_map_{}.npy'.format(filename)), btdepth_map)    
        
        np.save( os.path.join(os.path.dirname(f), 'cushape_map_{}.npy'.format(filename)), cushape_map)        
        
    
    
        print("Number of extracted CTUs is : ", ind_global_trace)
    
        assert (ind_global_trace == size_npy), "The number of extracted partition samples is not coherent with the number of input frames"
    
        # assert (ind_global_ctu == size_npy), "The number of extracted CTU samples is not coherent with the number of input frames"
    
    
    
        # if -1 in ctu:
        #     raise Exception('-1 value is in CTU pixels')
    
        # if -1 in qt_map:
        #     raise Exception('-1 value is in QTdepth map')
    
        # if -1 in mt1_map:
        #     raise Exception('-1 value is in mt1 map')
    
        # if -1 in mt2_map:
        #     raise Exception('-1 value is in mt2 map')
    
    
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










