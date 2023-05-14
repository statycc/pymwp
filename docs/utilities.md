# Utilities

There are several utility scripts in the repository `utilities` directory. These utilities mainly help to inspect, test,
and measure performance of pymwp in different ways. These tools are not shipped with the distributed version of pymwp;
they are only available from the development repository.

## List of Utilities

!!! info " "

    : :one: &nbsp; **AST Generator** (`ast_util.py`)<br/>Uses PyCParser to generate an AST of C files. It is useful for debugging, testing, and inspecting AST structure.
    
    : :two: &nbsp; **Results Plotter** (`plot.py`)<br/>Make plots of analyzer results. This is useful for benchmarking and inspecting performance. This scripts takes as input a directory path to pymwp results (output by default), then generates a table of those results.

    : :three: &nbsp; **Execution Profiling** (`profiler.py`)<br/>Profiler inspectes execution of various functions. It is helpful to locate bottlenecks and to understand analyzer function call structure.  

    : :four: &nbsp; **Machine Details** (`runtime.py`)<br/>Captures details of executing machine &mdash; useful for reporting results of benchmarking or profiling.

## Getting started

To run utilities, first install required dependencies:

```
python -m pip install -r requirements-test.txt
```

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

## Results Plotter

Makes a table plot of analysis results.

**Usage**

```
python3 utilities/plot.py [ARGS]
```

Run `python3 utilities/plot.py --help` for more assistance.

---

## Execution Profiling

Profiling shows how many times different functions are called during analysis. Profiling is carried out using
[cProfile](https://docs.python.org/3/library/profile.html#module-cProfile). You can profile execution of analysis on a
single file or multiple files.

<h3>Single file</h3>

This option can be used with pymwp installed from package registry or when running from source.

```
python -m cProfile -s ncalls pymwp path/to_some_file.c --silent
```

- use `-m pymwp` if running from source
- use `-s` to specify cProfile output sort order (
  cf. [options](https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats))
- use `--silent` to mute analysis output

<h3>Multiple file</h3>

Utility module [`profiler.py`](https://github.com/statycc/pymwp/blob/main/utilities/profiler.py) is a wrapper for
cProfile. This utility is not distributed with pymwp package - it must be run from source.

It enables profiling multiple executions of analysis on a _directory_ of C files (it recursively searches for C files).
The results of each execution are stored in corresponding files.

1. Run with defaults:

    ```
    make profile
    ```    

   <small>Default behavior is to profile all repository examples.</small>

2. Run with custom arguments:

    ```
    python utilities/profiler.py {args}
    ```

3. To see a list of available args:

    ```
    python utilities/profiler.py --help
    ```

1 of 3 possible outputs is displayed for each profiled execution:

- done-ok : profiling subprocess terminated without error, note: even if analysis ends with non-0 exit code, it falls
  into this category if it does not crash the process.
- error : profiling subprocess terminated in error.
- timeout : profiling subprocess did not terminate within time limit and was forced to quit.

---

## Machine Details

Captures e.g., hardware details for executing machine.

**Usage**

```
python3 utilities/runtime.py [output_dir]
```

Where `output_dir` specifies a directory where to write the machine details. 
