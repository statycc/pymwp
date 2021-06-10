# pymwp: MWP analysis in Python

[![build](https://github.com/seiller/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/seiller/pymwp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/seiller/pymwp/branch/master/graph/badge.svg?token=JHNYDJEWWM)](https://codecov.io/gh/seiller/pymwp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymwp)](https://pypi.org/project/pymwp/)
[![PyPI](https://img.shields.io/pypi/v/pymwp)](https://pypi.org/project/pymwp/)

Implementation of MWP analysis on C code in Python.

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

### Run analysis from source

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
    python -m pymwp path/to/c/file
    ```

    for example:
    
    ```bash
    python -m pymwp c_files/basics/if.c
    ```
    
    to see all available options see help
    
    ```bash
    python -m pymwp
    ```

<!--include-end--> 


