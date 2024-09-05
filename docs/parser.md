# parser.py

```python
from pymwp import Parser
```
 
Parser implementation is not a native part of pymwp. 
Parsing is implemented with [pycparser](https://github.com/eliben/pycparser).
The `Parser` module is simply a convenient wrapper. 
Enhancements and issues with C-file parsing are out of scope of pymwp.

::: pymwp.parser
    options:
      filters: ["!logger"]