'''
Created on 21 Jun 2022

@author: lukas
'''
import json
import hashlib

def dict_hash(dictionary):
    """MD5 hash of a dictionary."""
    
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    
    return dhash.hexdigest()

def load_grid_param(filepath):
    
    f = open(filepath)
    
    grid_dict = json.load(f)
    
    grid_param = {}

    for i in range(grid_dict['n_keys']):
        
        key = grid_dict[f'key_{i}']
        
        if type(key) == list:                                                
            grid_param[tuple(key)] = [grid_dict[f'grid_line_param_{i}{j}'] for j in range(len(key))]        
        else:
            grid_param[key] = grid_dict[f'grid_line_param_{i}']

    return grid_param, grid_dict['base_parameter']
