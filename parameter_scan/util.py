'''
Created on 21 Jun 2022

@author: lukas
'''
from os import path
import json
import hashlib
import numpy as np
import pickle

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

def load_file(data_path, 
              _hash, 
              prefix = '', 
              extension = '.dat',
              encoding = 'rb'):
    
    fn = prefix + _hash + extension     
    data = pickle.load(open(path.join(data_path, fn), encoding))
    
    return data

def load_file_grid(hash_grid, 
                   data_path, 
                   prefix = '', 
                   extension = '.dat',
                   encoding = 'rb'):

        if type(hash_grid) == list:
            s = (len(hash_grid),)
            hash_arr = hash_grid
        else:
            s = hash_grid.shape
            hash_arr = hash_grid.flatten()
                
        file_grid = np.zeros_like(hash_grid, dtype = np.object)
                
        for i, _hash in enumerate(hash_arr):
            idx = np.unravel_index(i, s)            
            data = load_file(data_path, _hash, prefix, extension, encoding)
            file_grid[idx] = data
                 
                                                    
        return file_grid

