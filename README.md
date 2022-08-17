# pymwp: MWP analysis in Python

[![build](https://github.com/statycc/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/statycc/pymwp/branch/main/graph/badge.svg?token=4v3zRbkAjM)](https://codecov.io/gh/statycc/pymwp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymwp)](https://pypi.org/project/pymwp/)
[![PyPI](https://img.shields.io/pypi/v/pymwp)](https://pypi.org/project/pymwp/)

<!--
    do not remove start and end comments (e.g. "include-start", "include-end").
    They are markers for what to include in the docs, but feel free to edit 
    the inner content.
-->

<!--desc-start-->

pymwp is a tool for automatically performing static analysis on programs written in C, inspired by [_"A Flow Calculus of mwp-Bounds for Complexity Analysis"_](https://doi.org/10.1145/1555746.1555752).
It analyzes resource usage and determines if a program's variables growth rates are no more than polynomially related to their inputs sizes.
You can run our [many examples](https://statycc.github.io/pymwp/examples/) on-line [in our demo](https://statycc.github.io/pymwp/demo/) before [installing it](https://statycc.github.io/pymwp/), consult our list of [supported C language features](https://statycc.github.io/pymwp/features/),
or review latest [profiling results](https://github.com/statycc/pymwp/releases/tag/profile-latest) for interesting metrics. 

<!--desc-end--> 

## Documentation and Demo

Refer to **[statycc.github.io/pymwp](https://statycc.github.io/pymwp/)** for a documentation of our modules, an [on-line demo](https://statycc.github.io/pymwp/demo/) as well as a presentation of [our examples](https://statycc.github.io/pymwp/examples/).

<!--include-start-->

## Installation

Install the latest release from PyPI

```bash
pip install pymwp
```

## How to Use

To analyze a C file, run:

```bash
pymwp path/to_some_file.c
```

For all available options and help, run:

```bash
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

See [modules documentation](https://statycc.github.io/pymwp/analysis/) for available methods.

## Running from source

If you want to use the latest stable version (possibly ahead of 
latest release), use the version from source following these steps.

1. Clone the repository

    ```
    git clone https://github.com/statycc/pymwp.git
    ``` 

2. Set up Python environment

    install required packages

    ```
    python -m pip install -q -r requirements.txt
    ``` 
    
    Note: for development purposes or to run tests, install dev dependencies instead: 
    
    ```
    python -m pip install -q -r requirements-dev.txt
    ```

3. Run the analysis

    From project root run:
    
    ```
    python -m pymwp path/to_some_file.c
    ```

    for example:
    
    ```
    python -m pymwp c_files/basics/if.c
    ```
    
    for all available options and help, run:
    
    ```
    python -m pymwp
    ```

<!--include-end--> 


