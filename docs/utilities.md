# Utilities

## Profiling

Profiling shows how many times different functions are called during analysis. Profiling is carried out using 
[cProfile](https://docs.python.org/3/library/profile.html#module-cProfile). You can profile execution of analysis on a single file or multiple files.

### Profiling single execution

This option can be used with installed package or when running from source.

```
python -m cProfile -s ncalls pymwp path/to_some_file.c --silent
```

- use `-m pymwp` if running from source
- use `-s` to specify cProfile output sort order (cf. [options](https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats))
- use `--silent` to mute analysis output

### Profiling multiple executions

[Profiler](https://github.com/seiller/pymwp/blob/master/utilities/profiler.py) is a wrapper for cProfile. It enables profiling multiple executions of analysis on a directory of C files (it will recursively search for C files). This utility is not distributed with pymwp package; you must run from source to use it.


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

- done : profiling subprocess terminated without error, note: even if analysis ends with non-0 exit code, it falls into this category if it does not crash the process.
- error : profiling subprocess terminated in error.
- timeout : profiling subprocess did not terminate within time limit and was forced to quit.
    
