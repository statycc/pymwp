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
It analyzes resource usage and determines if a program's variables growth rates are no more than polynomially related to
their inputs sizes.
It is inspired by [_"A Flow Calculus of mwp-Bounds for Complexity Analysis"_](https://doi.org/10.1145/1555746.1555752).
Try our online [demo](https://statycc.github.io/pymwp/demo/) to see it action.
For more details on usage and behavior, see pymwp [documentation](https://statycc.github.io/pymwp/), particularly [supported C language features](https://statycc.github.io/pymwp/features/).

<!--desc-end--> 

## Documentation and Demo

Refer to [statycc.github.io/pymwp](https://statycc.github.io/pymwp/) for technical documentation,
an [online demo](https://statycc.github.io/pymwp/demo/), and a presentation
of [examples](https://statycc.github.io/pymwp/examples/).

<!--include-start-->

For a publication, see ["pymwp: A Static Analyzer Determining Polynomial Growth Bounds"](http://doi.org/10.1007/978-3-031-45332-8_14)
also available on [HAL](https://hal.science/hal-03269121v4/document).

A comprehensive **tool user guide**, with detailed examples, is available at:
[statycc.github.io/.github/pymwp](https://statycc.github.io/.github/pymwp).
The user guide is the ideal place to start for a general and interactive introduction to pymwp.

## Installation

Install the latest release from PyPI

```
pip install pymwp
```

## How to Use

<h4>Command-Line Use</h4>

To analyze a C file, run in terminal:

```
pymwp path/to_some_file.c
```

For a list of available command options and help, run:

```
pymwp
```

<h4>Use in Python Scripts</h4>

You can also use pymwp by importing it in a Python script.

```python
from pymwp import Analysis, Parser
from pprint import pprint

# path to file to analyze
file = 'c_files/basics/if.c'

# parses a C-langugage file using pycparser
ast = Parser.parse(file, use_cpp=True, cpp_path='gcc')

# run analysis, then access result for main function
result = Analysis.run(ast, fin=True, no_save=True).get_func('main')

# display analysis result and collected data
pprint(result.to_dict())
```

See [modules documentation](https://statycc.github.io/pymwp/modules/) for details and examples.


## Running from source

If you want to use the latest stable version—possibly ahead of the latest release, and with special utilities and examples—use pymwp directly from source.

1. **Clone the repository**

    ```
    git clone https://github.com/statycc/pymwp.git 
    cd pymwp
    ``` 

2. **Set up Python runtime environment of preference**

    * :a: Using [Python venv&nearr;](https://docs.python.org/3/library/venv.html)
   
        Create and activate a virtual environment (POSIX bash/zsh):
     
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```
     
        Install required packages:
     
        ```
        python -m pip install -r requirements.txt
        ``` 
     
        For development, install dev-dependencies instead:
     
        ```
        python -m pip install -r requirements-dev.txt
        ```
      
    * :b: Using [Docker&nearr;](https://docs.docker.com/engine/install/)

        Build a container -- also installs dev-dependencies:
    
        ```
        docker build . -t pymwp
        ```
       
        Run the container:
    
        ```
        docker run --rm -v "$(pwd):$(pwd)" pymwp
        ```
 

4. **Run the analysis**

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
