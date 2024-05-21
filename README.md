# pymwp: MWP analysis in Python

[![build](https://github.com/statycc/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/statycc/pymwp/branch/main/graph/badge.svg?token=4v3zRbkAjM)](https://codecov.io/gh/statycc/pymwp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymwp)](https://pypi.org/project/pymwp/)
[![PyPI](https://img.shields.io/pypi/v/pymwp)](https://pypi.org/project/pymwp/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7879822.svg)](https://doi.org/10.5281/zenodo.7879822)


<!--
    do not remove start and end comments (e.g. "include-start", "include-end").
    They are markers for what to include in the docs, but feel free to edit 
    the inner content.
-->

<!--desc-start-->

pymwp is a tool for automatically performing static analysis on programs written in C.
It is inspired by [_"A Flow Calculus of mwp-Bounds for Complexity Analysis"_](https://doi.org/10.1145/1555746.1555752).
It analyzes resource usage and determines if a program's variables growth rates are no more than polynomially related to
their inputs sizes.
Try our online [demo](https://statycc.github.io/pymwp/demo/) to see it action.
For more details on usage and behavior, see pymwp [documentation](https://statycc.github.io/pymwp/),
particularly [supported C language features](https://statycc.github.io/pymwp/features/).

<!--desc-end--> 

## Documentation and Demo

Refer to **[statycc.github.io/pymwp](https://statycc.github.io/pymwp/)** for a documentation,
an [online demo](https://statycc.github.io/pymwp/demo/), and a presentation
of [examples](https://statycc.github.io/pymwp/examples/).

For a publication, see ["pymwp: A Static Analyzer Determining Polynomial Growth Bounds"](http://doi.org/10.1007/978-3-031-45332-8_14)
also available on [HAL](https://hal.science/hal-03269121v4/document).

<!--include-start-->

## Installation

Install the latest release from PyPI

```
pip install pymwp
```

## How to Use

To analyze a C file, run in terminal:

```
pymwp path/to_some_file.c
```

For all available options and help, run:

```
pymwp --help
```

<h4>Use in Python Scripts</h4>

You can also use pymwp by importing it in a Python script.
See [modules documentation](https://statycc.github.io/pymwp/analysis/) for available methods.

```python
from pymwp import Polynomial
from pymwp.matrix import identity_matrix, show

matrix = identity_matrix(3)
matrix[0][1] = Polynomial('m')
matrix[1][0] = Polynomial('w')
matrix[2][1] = Polynomial('p')

show(matrix)
```

## Tool User Guide

A comprehensive tool user guide, with detailed examples, is available at:
[statycc.github.io/.github/pymwp](https://statycc.github.io/.github/pymwp)


## Running from source

If you want to use the latest stable version (possibly ahead of the latest release), use the version from source
following these steps.

1. Clone the repository

    ```
    git clone https://github.com/statycc/pymwp.git
    ``` 

2. Set up Python environment (use [`venv`](https://docs.python.org/3/library/venv.html))

    install required packages

    ```
    python -m pip install -r requirements.txt
    ``` 

    For development and testing, install dev dependencies instead:

    ```
    python -m pip install -r requirements-dev.txt
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
