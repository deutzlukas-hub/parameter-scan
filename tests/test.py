'''
Created on 21 Jun 2022

@author: lukas
'''

import numpy as np

from parameter_scan.parameter_scan import ParameterGrid
from parameter_scan.util import load_grid_param

def dummy_base_parameter():
    
    base_parameter = {}

    base_parameter['a'] = 1.0
    base_parameter['b'] = 2.0
    base_parameter['c'] = 3.0
    base_parameter['d'] = 4.0
    
    return base_parameter
        
def test_line_grid_1():
        
    base_parameter = dummy_base_parameter()
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    
    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    
    grid_param = {'a': a_param}

    PG = ParameterGrid(base_parameter, grid_param)
    
    assert PG.keys == 'a'
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose(PG.v_arr, a_arr))
    
    assert np.all(np.isclose([p['a'] for p in PG.param_grid], a_arr)) 
    assert np.all(dict_hash(p) == fn for p, fn in zip(PG.param_grid, PG.filenames))
    
    print('ParameterGrid and LineGrid class passed test 1')
    
    return
        
def test_line_grid_2():

    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 20, 'step': None, 'round': 0, 'log': None}
    
    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
            
    grid_param = {('a', 'b'): [a_param, b_param]}

    PG = ParameterGrid(base_parameter, grid_param)
    
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose([v[0] for v in PG.v_arr], a_arr))
    assert np.all(np.isclose([v[1] for v in PG.v_arr], b_arr))
        
    assert np.all(np.isclose([p['a'] for p in PG.param_grid], a_arr)) 
    assert np.all(np.isclose([p['b'] for p in PG.param_grid], b_arr)) 
    assert np.all(dict_hash(p) == fn for p, fn in zip(PG.param_grid, PG.filenames))
        
    print('ParameterGrid and LineGrid class passed test 2')
        
def test_volume_grid_1():
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None}
    c_param = {'v_min': 0.0, 'v_max': 10, 'N': 10, 'step': None, 'round': 1, 'log': True}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])

    grid_param = {'a': a_param, 'b': b_param, 'c': c_param}

    PG = ParameterGrid(base_parameter, grid_param)

    assert PG.keys == ['a', 'b', 'c']
    assert len(PG.v_arr) == 3
    assert np.all(np.isclose([v for v in PG.v_arr[0]], a_arr))
    assert np.all(np.isclose([v for v in PG.v_arr[1]], b_arr))
    assert np.all(np.isclose([v for v in PG.v_arr[2]], c_arr))

    param_arr = PG.param_grid.flatten()
    filenames = PG.filenames.flatten()
    
    for i, t in enumerate(PG.v_mat.flatten()):
        
        p = param_arr[i]
        assert p['a'] == t[0]
        assert p['b'] == t[1]
        assert p['c'] == t[2]
        assert dict_hash(p) == filenames[i]
        
    print('ParameterGrid and VolumeGrid class passed test 1')

def test_volume_grid_2():
    
    base_parameter = dummy_base_parameter()
    
    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True}

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

    param_arr = PG.param_grid.flatten()
    filenames = PG.filenames.flatten()

    for i, t in enumerate(PG.v_mat.flatten()):
        
        p = param_arr[i]
        assert p['a'] == t[0]
        assert p['b'] == t[1]
        assert p['c'] == t[2][0]
        assert p['d'] == t[2][1]
        assert dict_hash(p) == filenames[i]
                
    print('ParameterGrid and VolumeGrid class passed test 2')

def test_line_slicing():
    
    base_parameter = dummy_base_parameter()

    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 20, 'step': None, 'round': 0, 'log': None}
    
    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
            
    grid_param = {('a', 'b'): [a_param, b_param]}

    PG = ParameterGrid(base_parameter, grid_param)

    v_arr, param_grid, filenames = PG[2:-3:2]
    
    a_arr = a_arr[2:-3:2]
    b_arr = b_arr[2:-3:2]
    
    assert len(PG.v_arr) == a_param['N']
    assert np.all(np.isclose([v[0] for v in v_arr], a_arr))
    assert np.all(np.isclose([v[1] for v in v_arr], b_arr))
        
    assert np.all(np.isclose([p['a'] for p in param_grid], a_arr)) 
    assert np.all(np.isclose([p['b'] for p in param_grid], b_arr)) 
    assert np.all(dict_hash(p) == fn for p, fn in zip(param_grid, filenames))

    print('ParameterGrid and LineGrid passed slicing test')


def test_volume_slicing():
    
    base_parameter = dummy_base_parameter()

    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])
    d_arr = np.round(10**np.linspace(d_param['v_min'], d_param['v_max'], d_param['N']), d_param['round'])

    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)
    
    v_mat, v_arr, param_grid, filenames = PG[::2, 5:, :-2]
    
    a_arr = a_arr[::2]
    b_arr = b_arr[5:]
    c_arr = c_arr[:-2]
    d_arr = d_arr[:-2]
    
    assert PG.keys == ['a', 'b', ('c', 'd')]
    assert len(PG.v_arr) == 3
    assert np.all(np.isclose([v for v in v_arr[0]], a_arr))
    assert np.all(np.isclose([v for v in v_arr[1]], b_arr))
    assert np.all(np.isclose([v[0] for v in v_arr[2]], c_arr))
    assert np.all(np.isclose([v[1] for v in v_arr[2]], d_arr))
    
    param_arr = param_grid.flatten()
    filenames = filenames.flatten()
    
    for i, t in enumerate(v_mat.flatten()):
        
        p = param_arr[i]
        assert p['a'] == t[0]
        assert p['b'] == t[1]
        assert p['c'] == t[2][0]
        assert p['d'] == t[2][1]
        assert dict_hash(p) == filenames[i]    
    
    print('ParameterGrid and VolumeGrid passed slicing test')

def test_volume_save_and_load():

    base_parameter = dummy_base_parameter()

    a_param = {'v_min': 0.0, 'v_max': 1.0, 'N': 20, 'step': None, 'round': 2, 'log': None}
    b_param = {'v_min': 100, 'v_max': 1000, 'N': 10, 'step': None, 'round': 0, 'log': None}
    c_param = {'v_min': 0.0, 'v_max': 1, 'N': 5, 'step': None, 'round': 1, 'log': True}
    d_param = {'v_min': 3, 'v_max': 5, 'N': 5, 'step': None, 'round': 0, 'log': True}

    a_arr = np.round(np.linspace(a_param['v_min'], a_param['v_max'], a_param['N']), a_param['round'])    
    b_arr = np.round(np.linspace(b_param['v_min'], b_param['v_max'], b_param['N']), b_param['round'])
    c_arr = np.round(10**np.linspace(c_param['v_min'], c_param['v_max'], c_param['N']), c_param['round'])
    d_arr = np.round(10**np.linspace(d_param['v_min'], d_param['v_max'], d_param['N']), d_param['round'])

    grid_param = {'a': a_param, 'b': b_param, ('c', 'd'): [c_param, d_param]}

    PG = ParameterGrid(base_parameter, grid_param)
    
    _dir = '../test/'
    
    filename = PG.save(_dir)
    fp = _dir + filename + '.json'

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

    print('ParameterGrid and VolumeGrid passed save and load')

    return
    
if __name__ == '__main__':
    
    test_line_grid_1()
    test_line_grid_2()
    test_volume_grid_1()
    test_volume_grid_2()
    test_line_slicing()
    test_volume_slicing()
    test_volume_save_and_load()
    
    