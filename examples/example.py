'''
Created on 22 Jun 2022

@author: lukas
'''
from parameter_scan.parameter_scan import ParameterGrid

def dummy_base_parameter():

    base_parameter = {}
    
    # These are all simulation parameters
    base_parameter['a'] = 1.0
    base_parameter['b'] = 2.0
    base_parameter['c'] = 3.0
    base_parameter['d'] = 4.0
    base_parameter['d'] = -1.0
    base_parameter['f'] = -2.0

    return base_parameter

def example_line_grid():

    base_parameter = dummy_base_parameter()

    # These are the parameters we want to vary
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': False}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 20, 'step': None, 'round': 0, 'log': False}

    grid_param = {('a', 'b'): [a_param, b_param]}

    PG = ParameterGrid(base_parameter, grid_param)

    # Parameter names
    print(PG.keys)
    # Gird is line, therefore the parameter array is one dimensional 
    print(PG.v_arr)
        
    # In this example, the parameters a,b are varied simultaneously
    # and the entries in v_arr are tuples (a,b)  
    print(PG.v_arr[0])
    
    # For each grid point we have a parameter dictionary'
    print(PG.param_grid[0])
    # For each parameter dictionary a hash is created  
    # which can be used e.g. as a filename to save 
    # associated simulation results
    print(PG.hash_grid[0])

    return

def example_volume_grid():
    
    base_parameter = dummy_base_parameter()
    
    # These are the parameters we want to vary
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': False}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': False}
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
    # For each parameter dictionary a hash is created  
    # which can be used e.g. as a filename to save 
    # associated simulation results
    print(PG.hash_grid[0,0,0])    
    # Flattend parameter and hash arrays can be accessed via
    print(PG.param_arr[0])
    print(PG.hash_arr[0])
                
if __name__ == '__main__':
    
    example_line_grid()
    example_volume_grid()
    
    
    
    
    
    
    




