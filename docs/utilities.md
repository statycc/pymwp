# Evaluation Utilities

There are several make commands and utility scripts in the repository's `utilities` directory. 
They mainly help to inspect, test, and measure and report of performance of pymwp in different ways. 
These tools are not shipped with the distributed version of pymwp, but are available from the source code repository.

<div class="grid cards" markdown>

- :material-file-tree: &nbsp; [**AST Generator**](#ast-generator) <br/>Convert C files to ASTs using pycparser.
- :octicons-clock-16: &nbsp; [**Benchmarks**](#benchmarks)  <br/>Run benchmarks on all examples.
- :fontawesome-solid-computer: &nbsp; [**Machine Details**](#machine-details) <br/>Captures host machine details at runtime.
- :material-chart-box-outline: &nbsp; [**Plot Results**](#plot-results) <br/>Make table plots of pymwp results.
- :fontawesome-solid-flask-vial: &nbsp; [**Profiling**](#profiling) <br/>Inspect functions runtime execution details.

</div>

!!! tip "Required dependencies"

    First install required dependencies for running utilities:
    
    ```
    python -m pip install -r requirements-test.txt
    ```


## AST Generator

::: utilities.ast_util
    options:
      show_docstring_modules: true
      members: false

## Benchmarks

Run pymwp on all [examples](examples.md), capture the executing machine details, and plot the results.
This is "just" a simplified command to execute pymwp repeatedly followed by utilities.

**Usage**

```
make bench
```


## Machine Details

::: utilities.runtime
    options:
      show_docstring_modules: true
      members: false

## Plot Results

::: utilities.plot
    options:
      show_docstring_modules: true
      members: false

## Profiling

::: utilities.profiler
    options:
      show_docstring_modules: true
      members: false