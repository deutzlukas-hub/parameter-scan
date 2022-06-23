'''
Created on 22 Jun 2022

@author: lukas
'''
from parameter_scan.parameter_scan import ParameterGrid

def example_volume_grid():
    
    base_parameter = {}
    
    # These are all simulation parameters
    base_parameter['a'] = 1.0
    base_parameter['b'] = 2.0
    base_parameter['c'] = 3.0
    base_parameter['d'] = 4.0
    base_parameter['d'] = -1.0
    base_parameter['f'] = -2.0
    
    # These are the parameters we want to vary
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True}

    # We want to to create a 3 dimensional grid for parameter tuples (a, b, (c,d))
    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)

    # Parameter names
    print(PG.keys)
    # Parameter arrays which span the grid
    for i, v_arr in enumerate(PG.v_arr):
        print(f'{PG.keys[i]}: {v_arr}')
    
    # Grid is 3d matrix with (20,10,5) shape
    print(PG.v_mat.shape)
    # Grid entry are parameter tuples
    print(PG.v_mat[0,0,0])
    
    # For each grid point we have a parameter dictionary'
    print(PG.param_grid[0,0,0])
    # For each parameter dictionary we have hash which 
    # can be used as a filename
    print(PG.filenames[0,0,0])
    
if __name__ == '__main__':
    
    example_volume_grid()
    
    
    
    
    
    
    




