---
title: Binary Assignment
subtitle: This program shows that assigning a compounded expression to a variable results in correct analysis.
---

#### Analyzed Program

```c
int foo(int y1, int y2){
    y2 = y1 + y1;
} 
```

This program is simple, and it is straightforward to observe that its input variables
have polynomial growth rates, i.e., $y_1^\prime \leq y_1$ and  $y_2^\prime \leq 2y_1$.
From analysis perspective this example is interesting, because binary operations
introduce complex polynomials in the matrix.

#### CLI Command

<details>
<summary>Get this example</summary>

```console
wget https://raw.githubusercontent.com/statycc/pymwp/main/c_files/basics/assign_expression.c
```
</details>

```console
pymwp assign_expression.c
```

<p>
  <a class="btn btn-outline-secondary" data-bs-toggle="collapse"
    href="#outputLog" role="button" aria-expanded="false"
    aria-controls="outputLog">
    Show Command Output
  </a>
</p>
<div class="collapse" id="outputLog"><div class="card card-body fs-6">

```
DEBUG (analysis): started analysis
DEBUG (analysis): variables of foo: ['y1', 'y2']
DEBUG (analysis): computing relation...0 of 1
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (analysis): computing composition...0 of 1
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (choice): infinity paths: None
INFO (result): 
MATRIX
y1  |  +m  +p.delta(0,0)+p.delta(1,0)+w.delta(2,0)
y2  |  +o  +o
INFO (result): CHOICES: [[[0, 1, 2]]]
INFO (result): Total time: 0.0 s (1 ms)
INFO (file_io): saved result in output/assign_expression.json
```
</div></div>

#### Matrix

|          | `y1` |                    `y2`                     |
|----------|:----:|:-------------------------------------------:|
| **`y1`** | $m$  | $p.\delta(0,0)+p.\delta(1,0)+w.\delta(2,0)$ |
| **`y2`** | $0$  |                     $0$                     |

Valid choices

```
[[0, 1, 2]]
```

#### Discussion

The analysis correctly assigns a polynomial bound to the program.
Every choice yields a valid matrix. 

<br/><a class="btn btn-outline-primary" href="exponent.html" role="button">
Next: Exponential Program
</a>