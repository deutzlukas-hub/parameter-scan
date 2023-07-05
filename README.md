#Python package to create, save and load grids for parameter scans 

This is a python package to create, save and load parameter grids for parameter scans in which a subset of larger set of simulations parameters is varied. For each grid point a unique parameter dictionary is created which is hashable. The hashes can be used as a filename to save the simulation results associated with the parameter dictionary at each grid point. 

#Installation

First, you need a python 3.x enviroment. The only third-party packages required is numpy and pint.

The `parameter_scan` package can be installed into the active python environment using the setup.py. From the parameter-scan package directory run

```bash
# The e option adds a symbolic link of the parameter_scan package to site-packages directory of the active environment 
pip install -e . 
```

#Testing

Test the package installation by executing 

```bash
cd parameter_scan
python ./tests/test.py 
```

#Usage

The main interface is provided `ParameterGrid` class in the `parameter_scan.py` module. Example use cases can be found in `/examples/example.py`. 


