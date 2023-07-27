# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:55:03 2023

@author: yliu
"""

import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--dep', help='cushape of ref encoding', type=str, default='')
parser.add_argument('--ref', help='cushape of dep encoding', type=str, default='')
args = parser.parse_args()



cushape_dep = np.load(args.dep)

cushape_ref = np.load(args.ref)


        
width_comp = (cushape_dep[:, :, :, 0, :, :] <=  cushape_ref[:, :, :, 0, :, :])

height_comp = (cushape_dep[:, :, :, 1, :, :] <=  cushape_ref[:, :, :, 1, :, :])

proportion = np.sum(width_comp & height_comp) / (cushape_dep.size / 2) * 100

        
print('{:.2f}'.format(proportion))		