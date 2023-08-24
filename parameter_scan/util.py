'''
Created on 21 Jun 2022

@author: lukas
'''
from os import path
import copy
import json
import hashlib
import numpy as np
import pickle
from pint import Quantity, Unit

def make_hashable(_dict):

    hash_dict = copy.deepcopy(_dict)

    for k, v in hash_dict.items():
        # Numpy array to list
        if hasattr(v, 'dtype'):                    
            hash_dict[k] = v.item()
        # Quantity to list
        if isinstance(v, Quantity):
            if isinstance(v.magnitude, np.ndarray):
                hash_dict[k] = [v.magnitude.tolist(), str(v.units)]            
            else:
                hash_dict[k] = [v.magnitude, str(v.units)]
                                                                    
        # Dict to hashable dict
        if isinstance(v, dict):
            hash_dict[k] = make_hashable(v)
            
    return hash_dict
                            
def dict_hash(dict):
    """MD5 hash of a dict."""
    
    dict = make_hashable(dict)
                    
    dhash = hashlib.md5()
    encoded = json.dumps(dict, sort_keys=True).encode()
    dhash.update(encoded)
    
    return dhash.hexdigest()

def restore_dict(hash_dict):
    
    dict = copy.deepcopy(hash_dict)
    
    for k, v in hash_dict.items():
        # List to quantity
        if isinstance(v, list):
            if len(v)==2:
                try:
                    if isinstance(v[0], list):
                        v[0] = np.array(v[0])                                        
                    unit = ureg(v[1])
                    param[k] = v[0]*unit                     
                except:
                    continue    
                                                                                 
        # Dict to hashable dict
        if isinstance(v, dict):
            hash_dict[k] = restore_dict(v)

    return dict

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

    mask_hash_keys = [key for key in grid_dict.keys() if key.startswith('mask_hash_arr')]
    mask_dict_keys = [key for key in grid_dict.keys() if key.startswith('mask_dict')]

    if len(mask_hash_keys) > 0:
        
        hash_mask_arr_list = [grid_dict[key] for key in mask_hash_keys]
        mask_dict_list = [grid_dict[key] for key in mask_dict_keys]
                
        return grid_param, grid_dict['base_parameter'], hash_mask_arr_list, mask_dict_list
        
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

