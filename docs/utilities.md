# Utilities

## Profiling

Profiling shows how many times different functions are called during analysis.
Profiling is carried out using 
[cProfile](https://docs.python.org/3/library/profile.html#module-cProfile).
You can profile execution of analysis on a single file, or a list of files.
For sorting profiling stats, see [sort options](https://docs.python
.org/3/library/profile
.html#pstats.Stats.sort_stats).

### Profiling execution of analysis on multiple files

[Profiler](
https://github.com/seiller/pymwp/blob/master/utilities/profile.py) is a wrapper
for cProfile. It enables profiling multiple passes of analysis on multiple C
 files stored in some directory.

1. Run with defaults:

    ```
    make profile
    ```    

    <small>Default behavior is to profile all repository examples.</small>

2. Run with custom arguments:

    ```
    python utilities/profile.py {args}
    ```

3. To see a list of available args:

    ```
    python utilities/profile.py --help
    ```

### Profiling single execution

To profile execution of analysis of a single C file:

```
python -m cProfile -s ncalls -m pymwp path/to_some_file.c --silent
```

- use `-s` to specify cProfile output sort order
- use `--silent` to mute analysis output
