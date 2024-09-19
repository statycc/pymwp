# syntax.py

```python
from pymwp import Coverage, Variables
```

Various light syntactic pre-analyses/pre-processors.

* `Coverage` checks that input C file follows [supported language features](features.md).
    * Running pymwp with `--strict` flag ensures only passing inputs are analyzed.
    * Otherwise, unsupported commands are removed from AST before analysis.
* `FindLoops` recursively finds all loop-nodes in an AST.
* `Variables` recursively finds variables in an AST.

::: pymwp.syntax