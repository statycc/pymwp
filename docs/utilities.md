# Evaluation Utilities

There are several make commands and utility scripts in the repository's `utilities` directory. 
They mainly help to inspect, test, and measure and report of performance of pymwp in different ways. 
These tools are not shipped with the distributed version of pymwp, but are available from the source code repository.

## List of Utilities

!!! info " "

    : :material-file-tree: &nbsp; **AST Generator** (`ast_util.py`)<br/>Convert C files to ASTs using pycparser. It is useful for debugging, testing, and inspecting AST structure.
    
    : :octicons-clock-16: &nbsp; **Benchmarks** (`make bench`)<br/>Run benchmarks on all examples.

    : :fontawesome-solid-flask-vial: &nbsp; **Execution Profiling** (`profiler.py`)<br/>The Python cProfiler inspects execution of various functions at runtime. It is helpful to locate bottlenecks and to understand analyzer function call structure.  

    : :fontawesome-solid-computer: &nbsp; **Machine Details** (`runtime.py`)<br/>Captures details of executing machine, mainly useful for reporting evaluation results.

    : :material-chart-box-outline: &nbsp; **Results Plotter** (`plot.py`)<br/>Make table plots of analyzer results for a specified directory.


## Getting started

First install required dependencies for using utilities:

```
python -m pip install -r requirements-test.txt
```

---

## AST Generator

This is a utility script reads and parses C file(s), then generates an AST. It uses gcc and pycparser, then writes the
AST to a file. This script is mainly useful for generating/updating test cases for unit testing, or inspecting AST
structure and nodes.

**Usage**

```
python3 utilities/ast_util.py [ARG1] [ARG2]
```

Positional arguments (required):

1. input path -- give a C file, or path to a directory of C files
2. output directory -- where to save AST

Note the parser options are hard-coded, and assumes C file has no custom headers, and that gcc is a valid C compiler.

---

## Benchmarks

**Usage**

```
make bench
```

The command runs

- Benchmarks for all examples in `c_files`
- Captures the executing machine details
- Generates plots of the results

---

## Execution Profiling

Profiling reveals how many times different functions are called during analysis. Profiling is carried out using
[cProfile](https://docs.python.org/3/library/profile.html#module-cProfile). You can profile execution of analysis on a
single file or multiple files.

<h3>Single file</h3>

This option can be used with pymwp installed from package registry or when running from source,
since cProfile is a standard module of Python runtime.

**Usage**

```
python -m cProfile -s ncalls pymwp path/to_some_file.c --silent
```

- use `-m pymwp` if running pymwp from source
- use `-s` to specify cProfile output sort order (
  cf. [options](https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats))
- use `--silent` to mute analysis output

<h3>Multiple files</h3>

Utility module [`profiler.py`](https://github.com/statycc/pymwp/blob/main/utilities/profiler.py) is a wrapper for
cProfile. 
It enables profiling multiple executions of analysis on a _directory_ of C files (it recursively searches for C files).
The results of each execution are stored in corresponding files.

**Usage**

1. Run with defaults (profiles all repository examples)

    ```
    make profile
    ```

2. Run with custom arguments:

    ```
    python utilities/profiler.py {args}
    ```

3. To see a list of available args:

    ```
    python utilities/profiler.py --help
    ```

One outputs is displayed for each profiled execution (3 possibilities):

- `done-ok` : profiling subprocess terminated without error, note: even if analysis ends with non-0 exit code, it falls
  into this category if it does not crash the process.
- `error` : profiling subprocess terminated in error.
- `timeout` : profiling subprocess did not terminate within time limit and was forced to quit.

---

## Machine Details

Captures software and hardware details for executing machine.

**Usage**

```
python3 utilities/runtime.py [output_dir]
```

Where `output_dir` specifies a directory where to write the machine details. 

---

## Results Plotter

Makes a table plot of analysis results.

**Usage**

```
python3 utilities/plot.py [ARGS]
```

Run `python3 utilities/plot.py --help` for more assistance.
