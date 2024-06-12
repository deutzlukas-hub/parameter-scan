'''
Created on 21 Jun 2022

@author: lukas
'''

import numpy as np

from parameter_scan import ParameterGrid
from parameter_scan.util import dict_hash, load_grid_param 

def dummy_base_parameter():
    
    base_parameter = {}

    base_parameter['a'] = 1.0
    base_parameter['b'] = 2.0
    base_parameter['c'] = 3.0
    base_parameter['d'] = 4.0
    
    return base_parameter
        
def test_line_grid_1():
        
    base_parameter = dummy_base_parameter()
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': 1.5}
    
    a_arr = np.round(a_param['scale'] * np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    
    grid_param = {'a': a_param}

    PG = ParameterGrid(base_parameter, grid_param)
    
    assert PG.keys == 'a'
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose(PG.v_arr, a_arr))
    
    assert np.all(np.isclose([p['a'] for p in PG.param_grid], a_arr)) 
    assert np.all(dict_hash(p) == fn for p, fn in zip(PG.param_grid, PG.hash_grid))
    
    print('ParameterGrid and LineGrid class passed test 1')
    
    return
        
def test_line_grid_2():

    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 20, 'step': None, 'round': 0, 'log': None, 'scale': None}
    
    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
            
    grid_param = {('a', 'b'): [a_param, b_param]}

    PG = ParameterGrid(base_parameter, grid_param)
    
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose([v[0] for v in PG.v_arr], a_arr))
    assert np.all(np.isclose([v[1] for v in PG.v_arr], b_arr))
        
    assert np.all(np.isclose([p['a'] for p in PG.param_grid], a_arr)) 
    assert np.all(np.isclose([p['b'] for p in PG.param_grid], b_arr)) 
    assert np.all(dict_hash(p) == fn for p, fn in zip(PG.param_grid, PG.hash_grid))
        
    print('ParameterGrid and LineGrid class passed test 2')
        
def test_line_grid_3():

    base_parameter = dummy_base_parameter()

    N = 20
    M = int(N/2)
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': N, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_tup': (1.0, 2.0), 'N_tup': (M, M), 'round': 0, 'log': None, 'scale': None}
             
    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])        
    b_arr = b_param['N_tup'][0]*[b_param['v_tup'][0]] + b_param['N_tup'][1]*[b_param['v_tup'][1]]

    grid_param = {('a', 'b'): [a_param, b_param]}
                        
    PG = ParameterGrid(base_parameter, grid_param)
    
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose([v[0] for v in PG.v_arr], a_arr))
    assert np.all(np.isclose([v[1] for v in PG.v_arr], b_arr))
        
    assert np.all(np.isclose([p['a'] for p in PG.param_grid], a_arr)) 
    assert np.all(np.isclose([p['b'] for p in PG.param_grid], b_arr)) 
    assert np.all(dict_hash(p) == fn for p, fn in zip(PG.param_grid, PG.hash_grid))

    print('ParameterGrid and LineGrid class passed test 3')

def test_volume_grid_1():
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': 0.5}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 10, 'N': 10, 'step': None, 'round': 1, 'log': True, 'scale': None}

    a_arr = np.round(a_param['scale']*np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])

    grid_param = {'a': a_param, 'b': b_param, 'c': c_param}

    PG = ParameterGrid(base_parameter, grid_param)

    assert PG.keys == ['a', 'b', 'c']
    assert len(PG.v_arr) == 3
    assert np.all(np.isclose([v for v in PG.v_arr[0]], a_arr))
    assert np.all(np.isclose([v for v in PG.v_arr[1]], b_arr))
    assert np.all(np.isclose([v for v in PG.v_arr[2]], c_arr))

    for i, t in enumerate(PG.v_mat.flatten()):
        
        p = PG.param_arr[i]
        assert p['a'] == t[0]
        assert p['b'] == t[1]
        assert p['c'] == t[2]
        assert dict_hash(p) == PG.hash_arr[i]
        
    print('ParameterGrid and VolumeGrid class passed test 1')

    return

def test_volume_grid_2():
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True, 'scale': None}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True, 'scale': None}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])
    d_arr = np.round(10**np.linspace(d_param['v_min'], d_param['v_max'], d_param['N']), d_param['round'])

    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)

    assert PG.keys == ['a', 'b', ('c', 'd')]
    assert len(PG.v_arr) == 3
    assert np.all(np.isclose([v for v in PG.v_arr[0]], a_arr))
    assert np.all(np.isclose([v for v in PG.v_arr[1]], b_arr))
    assert np.all(np.isclose([v[0] for v in PG.v_arr[2]], c_arr))
    assert np.all(np.isclose([v[1] for v in PG.v_arr[2]], d_arr))

    for i, t in enumerate(PG.v_mat.flatten()):
        
        p = PG.param_arr[i]
        assert p['a'] == t[0]
        assert p['b'] == t[1]
        assert p['c'] == t[2][0]
        assert p['d'] == t[2][1]
        assert dict_hash(p) == PG.hash_arr[i]
                
    print('ParameterGrid and VolumeGrid class passed test 2')

def test_volume_grid_3():
    
    base_parameter = dummy_base_parameter()

    N = 20
    M = int(N/2)
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': N, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': N, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_tup': (1.0, 2.0), 'N_tup': (M, M), 'round': 0, 'log': None, 'scale': None}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.array(c_param['N_tup'][0]*[c_param['v_tup'][0]] + c_param['N_tup'][1]*[c_param['v_tup'][1]])

    grid_param = {'a': a_param, ('b', 'c'): (b_param, c_param)}

    PG = ParameterGrid(base_parameter, grid_param)

    assert PG.keys == ['a', ('b', 'c')]
    assert len(PG.v_arr) == 2
    assert np.all(np.isclose([v for v in PG.v_arr[0]], a_arr))
    assert np.all(np.isclose([v[0] for v in PG.v_arr[1]], b_arr))
    assert np.all(np.isclose([v[1] for v in PG.v_arr[1]], c_arr))

    for i, t in enumerate(PG.v_mat.flatten()):
        
        p = PG.param_arr[i]
        assert p['a'] == t[0]
        assert p['b'] == t[1][0]
        assert p['c'] == t[1][1]
        assert dict_hash(p) == PG.hash_arr[i]
                
    print('ParameterGrid and VolumeGrid class passed test 3')


def test_line_grid_slicing():
    
    base_parameter = dummy_base_parameter()

    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 20, 'step': None, 'round': 0, 'log': None, 'scale': None}
    
    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
            
    grid_param = {('a', 'b'): [a_param, b_param]}

    PG = ParameterGrid(base_parameter, grid_param)

    idx_mat = PG[2:-3:2]
        
    a_arr = a_arr[2:-3:2]
    b_arr = b_arr[2:-3:2]
    
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose(PG.v_from_key('a')[idx_mat], a_arr))
    assert np.all(np.isclose(PG.v_from_key('b')[idx_mat], b_arr))
        
    assert np.all(np.isclose([p['a'] for p in PG.param_arr[idx_mat]], a_arr)) 
    assert np.all(np.isclose([p['b'] for p in PG.param_arr[idx_mat]], b_arr)) 
    assert np.all(dict_hash(p) == h for p, h in zip(PG.param_arr[idx_mat], PG.hash_arr[idx_mat]))

    print('ParameterGrid and LineGrid passed slicing test')

def test_volume_grid_slicing():
    
    base_parameter = dummy_base_parameter()

    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True, 'scale': None}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True, 'scale': None}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])
    d_arr = np.round(10**np.linspace(d_param['v_min'], d_param['v_max'], d_param['N']), d_param['round'])

    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)
    
    idx_mat = PG[::2, 5:, :-2]
    
    a_arr = a_arr[::2]
    b_arr = b_arr[5:]
    c_arr = c_arr[:-2]
    d_arr = d_arr[:-2]
    
    assert PG.keys == ['a', 'b', ('c', 'd')]
    assert len(PG.v_arr) == 3
    assert np.all(np.isclose(np.unique(PG.v_from_key('a')[idx_mat[0].flatten()]), a_arr))
    assert np.all(np.isclose(np.unique(PG.v_from_key('b')[idx_mat[1].flatten()]), b_arr))
    assert np.all(np.isclose(np.unique(PG.v_from_key('c')[idx_mat[2].flatten()]), c_arr))
    assert np.all(np.isclose(np.unique(PG.v_from_key('d')[idx_mat[2].flatten()]), d_arr))
        
    v_mat = PG.v_mat[idx_mat[0, :].flatten(),
        idx_mat[1, :].flatten(),
        idx_mat[2, :].flatten()].reshape(idx_mat.shape[1:])
        
    assert np.all(np.equal(v_mat, PG.v_mat[::2, 5:, :-2]))
        
    print('ParameterGrid and VolumeGrid passed slicing test')

def test_volume_grid_save_and_load():

    base_parameter = dummy_base_parameter()

    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True, 'scale': None}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True, 'scale': None}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])
    d_arr = np.round(10**np.linspace(d_param['v_min'], d_param['v_max'], d_param['N']), d_param['round'])

    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)
    
    _dir = './'
    
    fp = PG.save(_dir)

    grid_param_2, _ = load_grid_param(fp)
    a_param_2 = grid_param_2['a']
    b_param_2 = grid_param_2['b']
    cd_param_2 = grid_param_2[('c', 'd')]
    c_param_2 = cd_param_2[0]
    d_param_2 = cd_param_2[1]
    
    a_arr_2 = np.round(np.linspace(a_param_2['v_min'], a_param_2['v_max'], a_param_2['N']), a_param_2['round'])    
    b_arr_2 = np.round(np.linspace(b_param_2['v_min'], b_param_2['v_max'], b_param_2['N']), b_param_2['round'])
    c_arr_2 = np.round(10**np.linspace(c_param_2['v_min'], c_param_2['v_max'], c_param_2['N']), c_param_2['round'])
    d_arr_2 = np.round(10**np.linspace(d_param_2['v_min'], d_param_2['v_max'], d_param_2['N']), d_param_2['round'])

    assert np.all(np.isclose(a_arr, a_arr_2))
    assert np.all(np.isclose(b_arr, b_arr_2))
    assert np.all(np.isclose(c_arr, c_arr_2))
    assert np.all(np.isclose(d_arr, d_arr_2))

    print('ParameterGrid and VolumeGrid passed save and load test')

    return
    
def test_apply_mask_line_grid():
    
    base_parameter = dummy_base_parameter()
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': 1.5}
        
    grid_param = {'a': a_param}

    PG = ParameterGrid(base_parameter, grid_param)
        
    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG), int(len(PG)/3), replace = False)    
    hash_mask_arr = np.array(PG.hash_arr)[idx_arr]                            
    PG.apply_mask(hash_mask_arr, b = 10*base_parameter['b'])
             
    assert np.all(np.isclose([param['b'] for param in PG.param_arr[idx_arr] ], 10*base_parameter['b'])) 
    assert np.all(np.isclose([param['b'] for param in PG.param_grid[idx_arr]], 10*base_parameter['b'])) 

    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG), int(len(PG)/3), replace = False)    
    hash_mask_arr = np.array(PG.hash_arr)[idx_arr]                            
    PG.apply_mask(hash_mask_arr, b = 100*base_parameter['b'])

    assert np.all(np.isclose([param['b'] for param in PG.param_arr[idx_arr] ], 100*base_parameter['b'])) 
    assert np.all(np.isclose([param['b'] for param in PG.param_grid[idx_arr]], 100*base_parameter['b'])) 
            
    print('ParameterGrid and LineGrid passed apply_mask test')
    
    return

def test_apply_mask_volume_grid():
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': 0.5}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 10, 'N': 10, 'step': None, 'round': 1, 'log': True, 'scale': None}

    grid_param = {'a': a_param, 'b': b_param, 'c': c_param}

    PG = ParameterGrid(base_parameter, grid_param)

    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG), int(len(PG)/3), replace = False)    
    hash_mask_arr = np.array(PG.hash_arr)[idx_arr]                        
    PG.apply_mask(hash_mask_arr, d = 10 * base_parameter['d'])
    
    assert np.all(np.isclose([param['d'] for param in PG.param_arr[idx_arr] ], 10*base_parameter['d'])) 
    assert np.all(np.isclose([param['d'] for param in PG.param_grid.flatten()[idx_arr]], 10*base_parameter['d'])) 

    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG), int(len(PG)/3), replace = False)    
    hash_mask_arr = np.array(PG.hash_arr)[idx_arr]                        
    PG.apply_mask(hash_mask_arr, d = 100 * base_parameter['d'])
    
    assert np.all(np.isclose([param['d'] for param in PG.param_arr[idx_arr] ], 100*base_parameter['d'])) 
    assert np.all(np.isclose([param['d'] for param in PG.param_grid.flatten()[idx_arr]], 100*base_parameter['d'])) 

    print('ParameterGrid and VolumeGrid passed apply_mask test')
    
    return
    
def test_save_load_line_grid_with_mask(): 

    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 20, 'step': None, 'round': 0, 'log': None, 'scale': None}
                
    grid_param = {('a', 'b'): [a_param, b_param]}

    PG_1 = ParameterGrid(base_parameter, grid_param)
                            
    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG_1), int(len(PG_1)/5), replace = False)    
    hash_mask_arr = np.array(PG_1.hash_arr)[idx_arr]                        
    PG_1.apply_mask(hash_mask_arr, c = 10 * base_parameter['c'])
    
    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG_1), int(len(PG_1)/5), replace = False)    
    hash_mask_arr = np.array(PG_1.hash_arr)[idx_arr]                        
    PG_1.apply_mask(hash_mask_arr, c = 100 * base_parameter['c'])

    _dir = './'
    fp = PG_1.save(_dir)

    PG_2 = ParameterGrid.init_pg_from_filepath(fp)

    assert PG_1.filename == PG_2.filename 

    for param1, param2 in zip(PG_1.param_arr, PG_2.param_arr):
        
        for key in param1.keys():            
            assert param1[key] == param2[key]
        
    for param1, param2 in zip(PG_1.param_grid.flatten(), PG_2.param_grid.flatten()):
        
        for key in param1.keys():            
            assert param1[key] == param2[key]
        
    print('ParameterGrid and LineGrid with mask passed save and load test')

    return    
    
def test_save_load_volume_grid_with_mask(): 
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': 0.5}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 10, 'N': 10, 'step': None, 'round': 1, 'log': True, 'scale': None}

    grid_param = {'a': a_param, 'b': b_param, 'c': c_param}

    PG_1 = ParameterGrid(base_parameter, grid_param)

    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG_1), int(len(PG_1)/500), replace = False)    
    hash_mask_arr = np.array(PG_1.hash_arr)[idx_arr]                        
    PG_1.apply_mask(hash_mask_arr, d = 10 * base_parameter['d'])
    
    # select hashes for mask randomly                     
    idx_arr = np.random.choice(len(PG_1), int(len(PG_1)/500), replace = False)    
    hash_mask_arr = np.array(PG_1.hash_arr)[idx_arr]                        
    PG_1.apply_mask(hash_mask_arr, d = 100 * base_parameter['d'])

    _dir = './'
    fp = PG_1.save(_dir)

    PG_2 = ParameterGrid.init_pg_from_filepath(fp)

    assert PG_1.filename == PG_2.filename 

    for param1, param2 in zip(PG_1.param_arr, PG_2.param_arr):
        
        for key in param1.keys():            
            assert param1[key] == param2[key]
        
    for param1, param2 in zip(PG_1.param_grid.flatten(), PG_2.param_grid.flatten()):
        
        for key in param1.keys():            
            assert param1[key] == param2[key]
        
    print('ParameterGrid and VolumeGrid with mask passed save and load test')

    return
        
def test_has_key():
    
    base_parameter = dummy_base_parameter()
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': 1.5}    
    a_arr = a_param['scale'] * np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    
    grid_param = {'a': a_param}

    PG = ParameterGrid(base_parameter, grid_param)
    assert PG.has_key('a')
    assert not PG.has_key('b')
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None, 'scale': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None, 'scale': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True, 'scale': None}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True, 'scale': None}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])
    d_arr = np.round(10**np.linspace(d_param['v_min'], d_param['v_max'], d_param['N']), d_param['round'])

    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)

    PG = ParameterGrid(base_parameter, grid_param)
    
    assert PG.has_key('a')
    assert PG.has_key('b')
    assert PG.has_key('c')
    assert PG.has_key('d')
    assert not PG.has_key('e')

    print('ParameterGrid, LineGrid and VolumeGrid passed has_key test')
        
if __name__ == '__main__':
    
    test_line_grid_1()
    test_line_grid_2()
    test_line_grid_3()    
    test_volume_grid_1()
    test_volume_grid_2()
    test_volume_grid_3()    
    test_line_grid_slicing()
    test_volume_grid_slicing()
    test_volume_grid_save_and_load()
    test_apply_mask_line_grid()
    test_apply_mask_volume_grid()
    test_save_load_line_grid_with_mask()
    test_save_load_volume_grid_with_mask()
    test_has_key()
    
    
    