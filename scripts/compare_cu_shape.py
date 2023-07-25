# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:55:03 2023

@author: yliu
"""

import glob,os, sys
import numpy as np

files = sys.argv[1]


files_all = sorted(glob.glob(os.path.join(files, "*.npy")))


qps = [22, 27, 32, 37]

qp_numpys = []

for qp in qps:
    
    list_npys = []
    for f in files_all:
        if ('qp' + str(qp)) in f:
            list_npys.append(f)
        
    new = np.load(list_npys[0])
    
    for n in list_npys[1:]:
        
        new = np.concatenate((new, np.load(n)), axis=0)
    
    qp_numpys.append(new)

size = new.size / 2    

matrix = np.zeros((4, 4))


for ref in range(4):
    for dep in range(4):
        
        width_comp = (qp_numpys[dep][:, :, :, 0, :, :] <=  qp_numpys[ref][:, :, :, 0, :, :])
        
        height_comp = (qp_numpys[dep][:, :, :, 1, :, :] <=  qp_numpys[ref][:, :, :, 1, :, :])

        matrix[dep][ref] = np.sum(width_comp & height_comp) / size * 100
        
print(matrix)		