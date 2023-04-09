---
title: Exponential Program
subtitle: A program computing the exponentiation produces a matrix with infinite coefficient, no matter the choices.
---

#### Analyzed Program

```C
int main(int x, int n, int p, int r){
    p = x;
    while (n > 0)
    {
        if (n % 2 == 1)
            r = p * r;
        p = p * p;
        n = n / 2;
    }
}
```

This program variables `p` and `r` grow exponentially.
It is impossible to find a polynomial growth bound, and the analysis is expected to fail.
This example demonstrates how pymwp arrives to that conclusion.


#### CLI Command

<details>
<summary>Get this example</summary>

```console
wget https://raw.githubusercontent.com/statycc/pymwp/main/c_files/infinite/exponent_1.c
```
</details>

```console
pymwp exponent_1.c --fin
```

When run the analyzer with `--fin` argument, to have it run to completion and output a matrix. 
Without this flag, the analyzer terminates once it is known that no solution exists.


<p>
  <a class="btn btn-outline-secondary" data-bs-toggle="collapse" 
    href="#outputLog" role="button" aria-expanded="false"
    aria-controls="outputLog">
    Show Command Output
  </a>
</p>
<div class="collapse" id="outputLog"><div class="card card-body">

```
DEBUG (analysis): started analysis
DEBUG (analysis): variables of main: ['x', 'n', 'p', 'r']
DEBUG (analysis): computing relation...0 of 2
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation x = y
DEBUG (analysis): computing composition...0 of 2
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): computing relation...1 of 2
DEBUG (analysis): in compute_relation
DEBUG (analysis): analysing While
DEBUG (analysis): in compute_relation
DEBUG (analysis): computing relation (conditional case)
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): while loop fixpoint
DEBUG (relation): computing fixpoint for variables ['r', 'p', 'n']
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): fixpoint done ['r', 'p', 'n']
INFO (analysis): delta_graphs: infinite -> Exit now
DEBUG (analysis): computing composition...1 of 2
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
INFO (result): 
MATRIX
x  |  +m  +o  +m+i.delta(0,2)+i.delta(1,2)+i.delta(2,2)  +i.delta(0,1)+i.delta(1,1)+i.delta(2,1)
n  |  +o  +m  +i.delta(0,2)+i.delta(1,2)+i.delta(2,2)  +i.delta(0,1)+i.delta(1,1)+i.delta(2,1)
p  |  +o  +o  +i.delta(0,2)+i.delta(1,2)+i.delta(2,2)  +i.delta(0,1)+i.delta(1,1)+i.delta(2,1)
r  |  +o  +o  +i.delta(0,2)+i.delta(1,2)+i.delta(2,2)  +m+i.delta(0,1)+i.delta(1,1)+i.delta(2,1)
INFO (result): RESULT: main is infinite
INFO (result): Total time: 0.0 s (9 ms)
INFO (file_io): saved result in output/exponent_1.json
```
</div></div>

#### Matrix

|         | `x` | `n` |                             `p`                              |                             `r`                              |
|---------|:---:|:---:|:------------------------------------------------------------:|:------------------------------------------------------------:|
| **`x`** | $m$ | $0$ | $m+\infty.\delta(0,2)+\infty.\delta(1,2)+\infty.\delta(2,2)$ |  $\infty.\delta(0,1)+\infty.\delta(1,1)+\infty.\delta(2,1)$  |
| **`n`** | $0$ | $m$ |  $\infty.\delta(0,2)+\infty.\delta(1,2)+\infty.\delta(2,2)$  |  $\infty.\delta(0,1)+\infty.\delta(1,1)+\infty.\delta(2,1)$  |
| **`p`** | $0$ | $0$ |  $\infty.\delta(0,2)+\infty.\delta(1,2)+\infty.\delta(2,2)$  |  $\infty.\delta(0,1)+\infty.\delta(1,1)+\infty.\delta(2,1)$  |
| **`r`** | $0$ | $0$ |  $\infty.\delta(0,2)+\infty.\delta(1,2)+\infty.\delta(2,2)$  | $m+\infty.\delta(0,1)+\infty.\delta(1,1)+\infty.\delta(2,1)$ |

Valid choices

```
NONE
```


#### Discussion

The matrix shows that the problematic variables  are `p` and `r`. 
In the program, there are two critical binary multiplication operations that introduce choices (inside the `while` loop, at indices 1 and 2).
No matter what choice is made, it is not possible to obtain an $\infty$-free result.
This concludes the program does not pass the analysis.

<br/><a class="btn btn-outline-primary" href="not_infinite3.html" role="button">
Next: While Analysis
</a>