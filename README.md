# pymwp: MWP analysis in Python

[![build](https://github.com/seiller/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/seiller/pymwp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/seiller/pymwp/branch/master/graph/badge.svg?token=JHNYDJEWWM)](https://codecov.io/gh/seiller/pymwp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymwp)](https://pypi.org/project/pymwp/)
[![PyPI](https://img.shields.io/pypi/v/pymwp)](https://pypi.org/project/pymwp/)

<!--desc-start-->

pymwp is a tool for automatically performing static analysis on 
programs written in C. It analyzes resource usage and determines if a 
program stays within polynomial bounds. See 
[this page](https://seiller.github.io/pymwp/features/) for a list of C 
language features that are currently supported by pymwp.

<!--desc-end--> 

* * *

### Documentation and Demo

**[seiller.github.io/pymwp](https://seiller.github.io/pymwp/)**

* * *

<!--
    do not remove the next comment ("include-start") or the ending 
    ("include-end"), it is a marker for what to include in the docs, but 
    feel free to edit the instructions inside these markers
-->

<!--include-start-->

## Installation

Install latest release from PyPI

```
pip install pymwp
```

## How to Use

To analyze a C file, run:

```
pymwp path/to_some_file.c
```

For all available options and help, run:

```
pymwp
```


You can also use pymwp in a Python script:

```python
from pymwp import Polynomial
from pymwp.matrix import identity_matrix, show

matrix = identity_matrix(3)
matrix[0][1] = Polynomial('m')
matrix[1][0] = Polynomial('w')
matrix[2][1] = Polynomial('p')

show(matrix)
```

See [documentation](https://seiller.github.io/pymwp/analysis) for available modules and methods.

## Running from source

If you want to use the latest stable version (possibly ahead of 
latest release), use the version from source following these steps.

1. Clone the repository

    ```bash
    git clone https://github.com/seiller/pymwp.git
    ``` 

2. Set up Python environment

    install required packages

    ```bash
    pip install -q -r requirements.txt
    ``` 

3. Run the analysis

    From project root run:
    
    ```bash
    python -m pymwp path/to_some_file.c
    ```

    for example:
    
    ```bash
    python -m pymwp c_files/basics/if.c
    ```
    
    for all available options and help, run:
    
    ```bash
    python -m pymwp
    ```

<!--include-end--> 


