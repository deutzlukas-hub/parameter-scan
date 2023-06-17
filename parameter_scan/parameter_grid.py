'''
Created on 9 Jun 2022

@author: lukas
'''
from os.path import isfile, join
import itertools as it
import numpy as np
import json

from parameter_scan.util import dict_hash, load_grid_param

class LineGrid():
    
    def __init__(self, key, grid_line_param):
        '''
        
        :param key:
        :param grid_line_param:
        '''
                    
        self.key = key
        self.v_arr_list = []        
        self.N = 0 
        self.M = 0

        if type(grid_line_param) == dict:            
            grid_line_param = [grid_line_param]
                                                            
        for grid_param in grid_line_param:
            
            self.add_key(grid_param)
                                                                    
        self.v_arr = self.get_line_vector()
        
        return

    def __getitem__(self, s):
        
        return self.v_arr[s]
        
    def add_key(self, grid_param):

        if 'v_min' in grid_param:

            v_min = grid_param['v_min']
            v_max = grid_param['v_max']
            N = grid_param['N']
            step = grid_param['step']

            if N is not None:
                v_arr = np.linspace(v_min, v_max, N)
            else:
                assert step is not None, 'N or step must be not None'
                v_arr = np.arange(v_min, v_max, step)

        elif 'v_tup' in grid_param:
            
            v_tup = grid_param['v_tup']
            N_tup = grid_param['N_tup']
                        
            v_arr = []
            
            for v, N in zip(v_tup, N_tup):
            
                v_arr += N*[v]
                
        elif 'v_arr' in grid_param:            
            v_arr = np.array(grid_param['v_arr'])
                        
        if 'log' in grid_param:                                                                                      
            if grid_param['log']:
                v_arr = 10**v_arr
        
        if 'inverse' in grid_param:
            if grid_param['inverse']:            
                v_arr = 1/v_arr
        
        if 'scale' in grid_param:            
            if grid_param['scale'] is not None:
                v_arr = grid_param['scale'] * v_arr
        
        if 'offset' in grid_param:            
            if grid_param['offset'] is not None:
                v_arr = v_arr + grid_param['offset']
        
        if grid_param['round'] is not None:
            v_arr = np.round(v_arr, grid_param['round'])
        
        if 'flip_lr' in grid_param:
            if grid_param['flip_lr']:
                v_arr = v_arr[::-1]
                        
        self.v_arr_list.append(v_arr)
        self.M = len(self.v_arr_list)

        if self.N == 0:
            self.N = len(v_arr)
        else:
            assert self.N == len(v_arr), 'New key must have same length'
                  
        return v_arr
                    
    def get_line_vector(self):
                                        
        if self.M == 1:
            v_arr = self.v_arr_list[0]
        else:                            
            v_arr = np.zeros(self.N, dtype = object) 
            
            for i in range(self.N):
                v_arr[i] = tuple([self.v_arr_list[j][i] for j in range(self.M)])
            
        return v_arr
    
class VolumeGrid():
    
    def __init__(self, line_grid_list):
        
        self.line_grid_list = line_grid_list
        self.key_list = [line_grid.key for line_grid in line_grid_list]

        self.v_mat, self.v_arr_list, self.key_list = self.get_grid_matrix() 
    
    def __getitem__(self, s):
                        
        return self.v_mat[s], [v_arr[ss] for v_arr, ss in zip(self.v_arr_list, s)]
                                    
    def get_grid_matrix(self):
        
        shape = tuple([line_grid.N for line_grid in self.line_grid_list])                            
        
        v_arr_list = [line_grid.get_line_vector() for line_grid in self.line_grid_list]
                        
        v_mat = np.zeros(shape, dtype = object)
        
        for i, tup in enumerate(it.product(*v_arr_list)):
                                
            v_mat[np.unravel_index(i, shape)] = tup
            
        return v_mat, v_arr_list, self.key_list
    
class ParameterGrid():
    
    @staticmethod
    def init_pg_from_filepath(filepath): 
            
        grid = load_grid_param(filepath)                    
        grid_param, base_parameter = grid[0], grid[1] 
                
        PG = ParameterGrid(base_parameter, grid_param)
                    
        # if len return tuple = 4, one or more masks have been applied 
        if len(grid) == 4:
            
            hash_mask_arr_list, mask_dict_list = grid[2], grid[3]

            for hash_mask_arr, mask_dict in zip(hash_mask_arr_list, mask_dict_list): 

                PG.apply_mask(hash_mask_arr, **mask_dict)
    
        return PG
     
    def __init__(self, base_parameter, grid_param):


        self.base_parameter = base_parameter                    
        self.grid_param = grid_param
                
        if len(grid_param) == 1:
            self.line = True            
            self.grid = LineGrid(list(grid_param.keys())[0], list(grid_param.values())[0])
            
        else:
            self.line = False                                        
            line_grid_list = [LineGrid(key, grid_line_param) for key, grid_line_param in grid_param.items()]
            self.grid = VolumeGrid(line_grid_list)
    
        self.param_grid, self.hash_grid = self.create_param_and_hash_grid()
        
        self.grid_dict = self.create_grid_dict()
        self.filename = dict_hash(self.grid_dict)
                
        # Hash mask
        self.hash_mask_arr_list = []
        self.mask_dict_list = []
        self.mask_idx_arr_list = []                
                                
        return
                
    def __getitem__(self, s):
        
        idx_mat = np.indices(self.shape)
                            
        idx_mat_out = []
        
        for idx in idx_mat:            
            idx_mat_out.append(idx[s])
        
        idx_mat_out = np.array(idx_mat_out)
        
        if self.line: idx_mat_out=idx_mat_out.flatten()
        
        return idx_mat_out

    def has_key(self, K, return_dim = False):
        
        keys = self.keys
        
        has_k = False
        
        if type(keys) == list:
            for dim, key in enumerate(keys):
                if type(key) == tuple:                 
                    if K in key: 
                        has_k = True 
                        break
                else: 
                    if key == K:
                        has_k = True
                        break
        else:
            dim = 0            
            if type(keys) == tuple:
                if K in keys:
                    has_k = True                    
            else: 
                if K == keys:
                    has_k = True
        
        if not return_dim:            
            return has_k
        else:
            return has_k, dim
        
    def flat_index(self, idx_mat):
        
        flat_idx_mat = np.zeros((idx_mat.shape[0], np.prod(idx_mat.shape[1:])), dtype = int)
        
        for i, idx_arr in enumerate(idx_mat):
            flat_idx_mat[i, :] = idx_arr.flatten()
            
        flat_idx_arr = np.zeros(flat_idx_mat.shape[1], dtype = int)
                
        for i, multi_idx in enumerate(flat_idx_mat.T):
            flat_idx_arr[i] = np.ravel_multi_index(multi_idx, self.shape)
                                    
        return flat_idx_arr
                    
    def __len__(self):
        if self.line:
            return len(self.param_grid)
        else:
            return np.size(self.param_grid)
    
    @property
    def shape(self):

        return self.param_grid.shape
    
    @property
    def dim(self):
        
        return self.param_grid.ndim
                                                      
    @property                            
    def keys(self):
        
        if self.line:
            return self.grid.key        
        else:
            return self.grid.key_list
        
    @property
    def v_arr(self):
        
        if self.line:
            return self.grid.v_arr
        else:
            return self.grid.v_arr_list
    
    @property                        
    def v_mat(self):
        
        assert not self.line 
     
        return self.grid.v_mat
    
    def v_from_key(self, key):
        
        kf = False # key found
        
        if self.line:
            keys_list = [self.keys]
            v_arr_list = [self.v_arr]
        else:
            keys_list = self.keys
            v_arr_list = self.v_arr
                    
        for i, keys in enumerate(keys_list):   
            if type(keys) == str:
                if keys == key:
                    v_arr = v_arr_list[i]
                    kf = True
                            
            elif type(keys) == tuple:
                if key in keys:
                    idx = keys.index(key)
                    v_arr = np.array([t[idx] for t in v_arr_list[i]])                    
                    kf = True
                                                                   
        assert kf, 'Key not found'
        
        return v_arr
    
    def v_mat_from_key(self, key):
                
        if self.line:
            return self.v_from_key(key)
        
        kf = False # key found
        keys_list = self.keys                    
        
        for i, keys in enumerate(keys_list):   
            
            if type(keys) == str:
                if keys == key:
                    kf = True
                    v_key_mat = np.vectorize(lambda tup: tup[i])(self.v_mat)                                                  
            elif type(keys) == tuple:
                if key in keys:
                    idx = keys.index(key)                                        
                    v_key_mat = np.vectorize(lambda tup: tup[i][idx])(self.v_mat)
                                                                           
        assert kf, 'Key not found'
                
        return v_key_mat
    
    @property
    def param_arr(self):
        
        if self.line:
            return self.param_grid
        else:
            return self.param_grid.flatten()
    
    @property
    def hash_arr(self):
        
        if self.line:
            return self.hash_grid
        else:
            return self.hash_grid.flatten()
        
    @property 
    def mask_idx_arr(self):
        
        return self.mask_idx_arr_list[-1]
                 
    @property
    def param_mask_arr(self):
        
        if not self.hash_mask_arr_list:
            return self.param_arr
        
        return self.param_arr[self.mask_idx_arr]
                
    @property
    def hash_mask_arr(self):
        
        if not self.hash_mask_arr_list:
            return self.hash_arr
        
        return self.hash_arr[self.mask_idx_arr]
                                                         
    def create_param_and_hash_grid(self):
                
        if self.line:
                                    
            param_grid = []
                        
            is_tuple = type(self.grid.key) == tuple
                                    
            for v in self.grid.v_arr:
                
                param = self.base_parameter.copy()
                
                if is_tuple: 
                    for i, v_i in enumerate(v):
                        param[self.grid.key[i]] = v_i
                else:
                    param[self.grid.key] = v
                             
                param_grid.append(param)
            
            param_grid = np.array(param_grid)            
            hash_grid = np.array([dict_hash(p) for p in param_grid])
                                                                                    
        else:        
            
            param_grid = np.zeros_like(self.grid.v_mat)
            hash_grid = np.zeros_like(self.grid.v_mat)
            
            for i, tup in enumerate(self.grid.v_mat.flatten()):
                
                idx = np.unravel_index(i, self.grid.v_mat.shape)
                
                param = self.base_parameter.copy()
                
                for i, v in enumerate(tup):
                    
                    key = self.grid.key_list[i]
                
                    if type(key) == tuple: 
                        for j, v_j in enumerate(v):
                            param[key[j]] = v_j
                    else:
                        param[key] = v

                param_grid[idx] = param
                hash_grid[idx] = dict_hash(param)
                
        return param_grid, hash_grid

    def create_grid_dict(self):

        grid_dict = {}

        grid_dict['n_keys'] = len(self.grid_param)
        
        # this needs to be done because json can't dump tuple keys
        for i, (key, grid_line_param) in enumerate(self.grid_param.items()):
            
            grid_dict[f'key_{i}'] = key
            
            if type(key) == tuple:   
                for j in range(len(key)):
                    grid_dict[f'grid_line_param_{i}{j}'] = grid_line_param[j]                                
            else:                     
                grid_dict[f'grid_line_param_{i}'] = grid_line_param
                
        grid_dict['base_parameter'] = self.base_parameter

        if hasattr(self, 'hash_mask_arr_list'):
            
            for i, (hash_mask_arr, mask_dict) in enumerate(zip(self.hash_mask_arr_list, self.mask_dict_list)):
            
                if isinstance(hash_mask_arr, np.ndarray):
                    hash_mask_arr = hash_mask_arr.tolist()
            
                grid_dict[f'mask_hash_arr_{i}'] = hash_mask_arr
                grid_dict[f'mask_dict_{i}'] = mask_dict
                
        return grid_dict
                                                                            
    def apply_mask(self, hash_mask_arr, **kwargs):
                
        for key in kwargs.keys():
            assert key in self.base_parameter
                                                                              
        self.hash_mask_arr_list.append(hash_mask_arr)
        self.mask_dict_list.append(kwargs)
        
        idx_arr = [np.argmax(_hash == np.array(self.hash_arr)) for _hash in hash_mask_arr]
        
        self.mask_idx_arr_list.append(idx_arr)
                                
        for idx in idx_arr:            
            param = self.param_arr[idx]            
            for key, value in kwargs.items():                    
                param[key] = value                
                idx = np.unravel_index(idx, self.param_grid.shape)
                
                self.param_grid[idx] = param
                self.hash_grid[idx] = dict_hash(param)
                        
        self.grid_dict = self.create_grid_dict()
        self.filename = dict_hash(self.grid_dict)
                        
        return

    def save(self, _dir, prefix = ''):
                
        fp  = join(_dir, prefix + self.filename + '.json')
        
        if isfile(fp):
            #print('Grid file already exists!')
            return fp
        
        with open(fp, 'w') as f:
        
            json.dump(self.grid_dict, f, indent=4)
        
        return fp
    
        
 