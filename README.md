# pymwp: MWP analysis in Python

[![build](https://github.com/seiller/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/seiller/pymwp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/seiller/pymwp/branch/master/graph/badge.svg?token=JHNYDJEWWM)](https://codecov.io/gh/seiller/pymwp)

Implementation of MWP analysis on C code in Python.

Source code documentation is available at [seiller.github.io/pymwp](https://seiller.github.io/pymwp/).

<!--
    do not remove the next comment ("include-start") or the ending 
    ("include-end"), it is a marker for what to include in the docs, but 
    feel free to edit the instructions...
-->

<!--include-start-->

### How to run the analysis

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

* * *

### Checking code changes

Any changes to source code must pass lint + unit tests and these are
checked automatically. Here are some helpful commands for checking your changes:

In the project root, run:

```text
make pre-commit   # check everything
```

```text
make test         # check unit tests only (1
```

```text
make lint         # check code style only (2
```

```text
make clean        # clean generated files
```


1) Unit tests are in `tests` directory. You can run unit tests on specific files or the entire source. 
See [pytest documentation](https://docs.pytest.org/en/stable/contents.html) for more details.

2) This project uses [flake8](https://flake8.pycqa.org/en/latest/index.html) for linting.
You can use it to check specific files or run it against all Python source files by specifying a path.
