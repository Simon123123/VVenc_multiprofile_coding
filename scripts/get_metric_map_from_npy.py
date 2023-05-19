import math
import os
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--npy', help='numpy array file to parse', type=str, default='cushape_map_trace_bqsquare_qp22.npy')
parser.add_argument('--path', help='Directory to generated maps', type=str, default='data')
parser.add_argument('--cell_size', help='Cell size of the CTU map', type=int, default=8)
parser.add_argument('--ctu_size', help='CTU size', type=int, default=128)
parser.add_argument('--metric', help='Metric to record from log (max_size_map_1d, max_size_map_2d, min_size_map_1d, min_size_map_2d, what else?)', type=str, default='max_size_1d')
args = parser.parse_args()


def main():
    check_log(args.npy)

    assert args.cell_size % 8 == 0 or args.cell_size == 4, "The size of cell should be 4 or a multiple of 8 !!"
    assert args.metric in ['max_size_map_1d', 'max_size_map_2d', 'min_size_map_1d', 'min_size_map_2d'], "Unvalid metric"
    
    list_files_trace = []
    
    for dirpath, dirnames, filenames in sorted(os.walk(args.npy)):
        for filename in [f for f in filenames if f.startswith("cushape")]:
            list_files_trace.append(os.path.join(dirpath, filename))

    for f in list_files_trace:
        
        filename = f.split(os.sep)[-1].split('.')[0]
        
        data = np.load(f).astype(np.int16)
        
        shape_w = data[:, :, :, 0, :, :]
        
        shape_h = data[:, :, :, 1, :, :]
        
        size_map = args.ctu_size // args.cell_size 
        
        ops_scale = args.cell_size // 4
        
        if args.metric in ['max_size_map_1d', 'max_size_map_2d']:
            shape_w = shape_w.reshape((shape_w.shape[0], shape_w.shape[1], shape_w.shape[2], size_map, ops_scale, size_map, ops_scale)).max(axis=(4, 6))
            shape_h = shape_h.reshape((shape_w.shape[0], shape_w.shape[1], shape_w.shape[2], size_map, ops_scale, size_map, ops_scale)).max(axis=(4, 6))
        else:
            shape_w = shape_w.reshape((shape_w.shape[0], shape_w.shape[1], shape_w.shape[2], size_map, ops_scale, size_map, ops_scale)).min(axis=(4, 6))
            shape_h = shape_h.reshape((shape_w.shape[0], shape_w.shape[1], shape_w.shape[2], size_map, ops_scale, size_map, ops_scale)).min(axis=(4, 6))        
        
        
        shape = 0
        if args.metric == 'max_size_map_1d':
            shape = np.maximum(shape_w, shape_h)
        elif args.metric == 'min_size_map_1d':
            shape = np.minimum(shape_w, shape_h)
        else:
            # shape = np.concatenate((shape_w, shape_h), axis = -1)
            shape = np.stack((shape_w, shape_h), axis = 3)
        
        shape = shape.reshape(-1, size_map*size_map)
        np.savetxt(os.path.join(args.path, args.metric + '_scale_' + str(args.cell_size) + '_' + filename + '.csv'), shape, fmt='%d', delimiter=';')
            
                    

def check_log(log_path):
    if not os.path.exists(log_path):
        print(f'Npy file does not exist ({log_path})')


if __name__ == '__main__':
    main()
