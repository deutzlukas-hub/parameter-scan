'''
Created on 23 Jun 2022

@author: lukas
'''

from setuptools import setup

ds = '''Module to create and save parameter grids for 
parameter scans in which a subset of larger set of simulations 
parameters is varied. For each grid point a unique parameter
dictionary which is hashable.  
The hash can be used as a filename to save the simulation results
associated with the respective parameter dictionary'''

setup(
    name = 'parameter_scan',
    version = '0.1',
    authoor = 'Lukas Deutz',
    author_email = 'scld@leeds.ac.uk',
    description = ds,
    url = 'https://github.com/LukasDeutz/parameter-scan.git',
    packages = ['parameter_scan']
)



                    