import math
import os
import argparse
import numpy as np
from common import *

parser = argparse.ArgumentParser()
parser.add_argument('--log', help='CSV log file to parse', type=str, default='trace_bqsquare_qp22.csv')
parser.add_argument('--path', help='Subdirectory to logs', type=str, default='data')
parser.add_argument('--cell_size', help='Cell size of the CTU map', type=int, default=8)
parser.add_argument('--metric', help='Metric to record from log (max_size_map_1d, max_size_map_2d, min_size_map_1d, min_size_map_2d, what else?)', type=str, default='max_size_1d')
args = parser.parse_args()


def main():
    log_path = os.path.join(args.path, args.log)
    check_log(log_path)

    data = np.loadtxt(log_path, delimiter=';').astype(np.int32)

    # Parameters
    poc = 0
    ctu_x = 2
    ctu_y = 1

    # Extract raw data
    data_ctu = get_lines_idx_ctu(data, poc, ctu_x, ctu_y)

    # Get metric map
    metric_map = get_metric_map_ctu(data_ctu, args.metric, args.cell_size)

    print(f'Map of {args.metric} is: \n{metric_map.astype(np.int32)}')


def get_metric_map_ctu(data, metric, cell_size):
    size_in_cell = ctu_size // cell_size
    dim = 1
    if metric == 'max_size_2d' or metric == 'min_size_2d':
        dim = 2
    metric_map = np.zeros((size_in_cell, size_in_cell, dim))
    for cu in data:
        update_map_with_cu(metric_map, cu, metric)

    return metric_map


def update_map_with_cu(metric_map, cu, metric):
    cu_x = cu[1] % ctu_size
    cu_y = cu[2] % ctu_size
    cu_width = cu[3]
    cu_height = cu[4]
    cell_size = ctu_size // metric_map.shape[0]  # dirty!
    start_x, end_x, start_y, end_y = get_concerned_cells_from_cu_coordinates(cu_x, cu_y, cu_width, cu_height, cell_size)

    if metric == 'max_size_1d':
        value = max(cu_width, cu_height)
    elif metric == 'min_size_1d':
        value = min(cu_width, cu_height)
    elif metric not in ['max_size_2d', 'min_size_2d']:
        print(f'ERROR: {metric} not implemented\nExiting.')
        exit(0)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if metric == 'max_size_1d':
                metric_map[y, x, 0] = max(metric_map[y, x, 0], value)
            elif metric == 'min_size_1d':
                metric_map[y, x, 0] = min(metric_map[y, x, 0], value)
            elif metric == 'max_size_2d':
                metric_map[y, x, 0] = max(metric_map[y, x, 0], cu_width)
                metric_map[y, x, 1] = max(metric_map[y, x, 1], cu_height)
            elif metric == 'min_size_2d':
                metric_map[y, x, 0] = min(metric_map[y, x, 0], cu_width)
                metric_map[y, x, 1] = min(metric_map[y, x, 1], cu_height)                
            else:
                print(f'ERROR: {metric} not implemented\nExiting.')
                exit(0)

    return metric_map


def get_concerned_cells_from_cu_coordinates(cu_x, cu_y, cu_width, cu_height, cell_size):
    start_x = cu_x // cell_size
    start_y = cu_y // cell_size
    end_x = math.ceil((cu_x + cu_width) / cell_size)
    end_y = math.ceil((cu_y + cu_height) / cell_size)
    return start_x, end_x, start_y, end_y


def get_lines_idx_ctu(data, poc, ctu_x, ctu_y):
    data = data[data[:, 0] == poc]
    ctu_start_x = ctu_x * ctu_size
    ctu_end_x = (ctu_x + 1) * ctu_size
    ctu_start_y = ctu_y * ctu_size
    ctu_end_y = (ctu_y + 1) * ctu_size

    data = data[data[:, 1] >= ctu_start_x]
    data = data[data[:, 1] < ctu_end_x]
    data = data[data[:, 2] >= ctu_start_y]
    data = data[data[:, 2] < ctu_end_y]
    return data


def derive_resolution(data):
    last_cu = data[-1]
    width = last_cu[1] + last_cu[3]
    height = last_cu[2] + last_cu[4]

    return width, height


def check_log(log_path):
    if not os.path.exists(log_path):
        print(f'Log file does not exist ({log_path})')


if __name__ == '__main__':
    main()
