# analysis.py

```python
from pymwp import Analysis
```

## Analyzing programs with custom headers

Programs with custom header files require passing the path to header file location(s) as a command line argument.
Use prefix `-I` followed by (relative or absolute) path to headers directory.
For example, if header file is in directory `my_headers` then the required command line argument is:

```text
python -m pyalp my_program.c --cpp_args="-Imy_headers"
```


::: pymwp.analysis
    selection:
      members:
        - Analysis