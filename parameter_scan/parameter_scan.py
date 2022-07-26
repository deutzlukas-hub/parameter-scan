'''
Created on 9 Jun 2022

@author: lukas
'''
import itertools as it
import numpy as np
import json

from parameter_scan.util import dict_hash

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
            
            self.add_key(grid_param['v_min'], 
                         grid_param['v_max'], 
                         grid_param['N'], 
                         grid_param['step'], 
                         grid_param['round'], 
                         grid_param['log'],
                         grid_param['scale'])
                                            
        self.v_arr = self.get_line_vector()
        
        return

    def __getitem__(self, s):
        
        return self.v_arr[s]
        
    def add_key(self, v_min, v_max, N=None, step = None, _round = None, log = False, scale = None):
                
        if N is not None:
            v_arr = np.linspace(v_min, v_max, N)
        else:
            assert step is not None, 'N or step must be not None'
            v_arr = np.arange(v_min, v_max, step)
                                                                        
        if log:
            v_arr = 10**v_arr
        
        if _round is not None:
            v_arr = np.round(v_arr, _round)
            
        if scale is not None:
            v_arr = scale * v_arr
        
        self.v_arr_list.append(v_arr)
        self.M = len(self.v_arr_list)

        if self.N == 0:
            self.N = len(v_arr)
        else:
            assert self.N == len(v_arr), 'New key must have same length'
        
        return
        
    def get_line_vector(self):
                                        
        if self.M == 1:
            v_arr = self.v_arr_list[0]
        else:                            
            v_arr = np.zeros(self.N, dtype = np.object) 
            
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
                        
        v_mat = np.zeros(shape, dtype = np.object)
        
        for i, tup in enumerate(it.product(*v_arr_list)):
                                
            v_mat[np.unravel_index(i, shape)] = tup
            
        return v_mat, v_arr_list, self.key_list
    
class ParameterGrid():
    
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
                
    def __getitem__(self, s):
        
        if self.line:            
            return self.grid[s], self.param_grid[s], self.hash_grid[s]            
        else:        
            v_mat, v_arr_list = self.grid[s]        
            return v_mat, v_arr_list, self.param_grid[s], self.hash_grid[s] 
    
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
            
            hash_grid = [dict_hash(p) for p in param_grid]
                                                                                    
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
                                                                    
    def save(self, _dir, prefix = ''):
        
        grid_dict = {}

        grid_dict['n_keys'] = len(self.grid_param)
        
        # this need to be done because json can't dump tuple keys
        for i, (key, grid_line_param) in enumerate(self.grid_param.items()):
            
            grid_dict[f'key_{i}'] = key
            
            if type(key) == tuple:   
                for j in range(len(key)):
                    grid_dict[f'grid_line_param_{i}{j}'] = grid_line_param[j]                                
            else:                     
                grid_dict[f'grid_line_param_{i}'] = grid_line_param
        
        grid_dict['base_parameter'] = self.base_parameter
        
        
        filename = dict_hash(grid_dict)
        
        with open(_dir + prefix + filename + '.json', 'w') as f:
        
            json.dump(grid_dict, f, indent=4)
        
        return filename
                    

