# pymwp: MWP analysis in Python

[![build](https://github.com/statycc/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/statycc/pymwp/branch/main/graph/badge.svg?token=4v3zRbkAjM)](https://codecov.io/gh/statycc/pymwp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymwp)](https://pypi.org/project/pymwp/)
[![PyPI](https://img.shields.io/pypi/v/pymwp)](https://pypi.org/project/pymwp/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7879822.svg)](https://doi.org/10.5281/zenodo.7879822)

<!-- 
  Do not remove start and end comments (e.g. "include-start", "include-end").
  They are markers for what to include in the documentation website.
-->

<!--include-start-->

pymwp is a tool for automatically performing static analysis on programs written in C.
It analyzes resource usage and determines if a program's variables growth rates are no more than polynomially related to
their inputs sizes. 

For example,

   ```c
   int main(int X1, int X2, int X3){
       X1 = X2 + X3;
       X1 = X1 + X1;
   }
   ``` 
   
   is satisfactory because—between the initial variable values (`Xi`) and the final values (`Xi'`)—all variables have a polynomially bounded data-flow (omitting constants): 
   `X1' ≤ X2+X3` and `X2' ≤ X2`  and `X3' ≤ X3`. pymwp derives this bound automatically ([⯈ demo](https://statycc.github.io/pymwp/demo/#original_paper_example3_1_b.c)).

However, program

   ```c
   int main(int X1, int X2, int X3){
      X1 = 1;
      while (X2 > 0){ X1 = X1 + X1; }
   }   
   ```

   fails the analysis, because `X1` grows exponentially (`X1'` = $2^{\texttt{X2}}$).
   pymwp reports a program is _infinite_ when no polynomial bound can be derived ([⯈ demo](https://statycc.github.io/pymwp/demo/#original_paper_example3_1_d.c)).


pymwp is inspired by [_"A Flow Calculus of mwp-Bounds for Complexity Analysis"_](https://doi.org/10.1145/1555746.1555752).
Try our online [demo](https://statycc.github.io/pymwp/demo/) to see it action.
For more details, see pymwp [documentation](https://statycc.github.io/pymwp/), particularly [supported C language features](https://statycc.github.io/pymwp/features/).

## Documentation and Demo

**Documentation:** [statycc.github.io/pymwp](https://statycc.github.io/pymwp/)

**Demo**: [online demo](https://statycc.github.io/pymwp/demo/) and [input examples](https://statycc.github.io/pymwp/examples/)

**Publication**: ["pymwp: A Static Analyzer Determining Polynomial Growth Bounds"](http://doi.org/10.1007/978-3-031-45332-8_14),
also on [HAL](https://hal.science/hal-03269121v4/document).

**Tool user guide**: [statycc.github.io/.github/pymwp](https://statycc.github.io/.github/pymwp) with detailed examples and discussion.

The user guide is the ideal place to start for a general and interactive introduction to pymwp.

## Installation

Install the latest release from PyPI

```
pip install pymwp
```

## How to Use

**Command-Line Use**

To analyze a C file, run in terminal:

```
pymwp path/to_some_file.c
```

For a list of available command options and help, run:

```
pymwp
```

**Use in Python Scripts**

You can also use pymwp by importing it in a Python script.
See [modules documentation](https://statycc.github.io/pymwp/modules/) for details and examples.

## Running from source

If you want to use the latest stable version—possibly ahead of the latest release, and with special [evaluation utilities](https://statycc.github.io/pymwp/utilities/) and [input examples](https://statycc.github.io/pymwp/examples/)—use pymwp directly from source.

1. **Clone the repository**

    ```shell
    git clone https://github.com/statycc/pymwp.git 
    cd pymwp
    ``` 

2. **Set up Python runtime environment of preference**

    :a: &nbsp; Using [Python venv&nearr;](https://docs.python.org/3/library/venv.html)
   
    Create and activate a virtual environment (POSIX bash/zsh):
     
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```
     
    Install required packages:
     
    ```shell
    python -m pip install -r requirements.txt
    ``` 
     
    For development, install dev-dependencies instead:
     
    ```shell
    python -m pip install -r requirements-dev.txt
    ```

    :b: &nbsp; Using [Docker&nearr;](https://docs.docker.com/engine/install/)

    Build a container -- also installs dev-dependencies:
    
    ```shell
    docker build . -t pymwp
    ```
       
    Run the container:
    
    ```shell
    docker run --rm -v "$(pwd):$(pwd)" pymwp
    ```
 

3. **Run the analysis**

    From project root run:

    ```shell
    python -m pymwp path/to_some_file.c
    ```

    for example:

    ```shell
    python -m pymwp c_files/basics/if.c
    ```

    for all available options and help, run:

    ```shell
    python -m pymwp
    ```

<!--include-end--> 


## Evaluation

These options are available when running from source.

```
make bench       # run benchmark of all c_files examples
make test        # run unit tests on pymwp source code
make profile     # run cProfile on all c_files examples  
```
