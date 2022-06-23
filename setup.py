'''
Created on 23 Jun 2022

@author: lukas
'''
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'parameter_scan',
    version = '0.1',
    author = 'Lukas Deutz',
    author_email = 'scld@leeds.ac.uk',
    description = 'Module to create, save and load parameter grids for parameter scans',
    long_description = read('README.md'),
    url = 'https://github.com/LukasDeutz/parameter-scan.git',
    packages = ['parameter_scan']
)



                    