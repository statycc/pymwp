---
title: While Analysis
subtitle: A program that shows infinite coefficients for some choices.
next: Infinite Program
next_href: example_infinite.html
---

#### Analyzed Program

```c
int foo(int X0, int X1, int X2, int X3){
    if (X1 == 1){
        X1 = X2+X1;
        X2 = X3+X2;
    }
    while(X0<10){
        X0 = X1+X2;
    }
}
```

This program contains decision logic, a while loop, and multiple variables.
Determining if a "polynomial growth bound" exists is not immediate by inspection.
It is therefore an interesting candidate for analysis with pymwp!


#### CLI Command

<details>
<summary>Get this example</summary>

```console
wget https://raw.githubusercontent.com/statycc/pymwp/main/c_files/not_infinite/notinfinite_3.c
```
</details>

```console
pymwp notinfinite_3.c
```

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
DEBUG (analysis): variables of foo: ['X0', 'X1', 'X2', 'X3']
DEBUG (analysis): computing relation...0 of 2
DEBUG (analysis): in compute_relation
DEBUG (analysis): computing relation (conditional case)
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): computing composition...0 of 2
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): computing relation...1 of 2
DEBUG (analysis): in compute_relation
DEBUG (analysis): analysing While
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): while loop fixpoint
DEBUG (relation): computing fixpoint for variables ['X0', 'X1', 'X2']
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): fixpoint done ['X0', 'X1', 'X2']
DEBUG (analysis): computing composition...1 of 2
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (choice): infinity paths: [(0, 2)] # [(1, 2)]
DEBUG (choice): maximum distinct vectors: 1
INFO (result): 
MATRIX
X0  |  +m+i.delta(0,2)+i.delta(1,2)  +o  +o  +o
X1  |  +p.delta(1,0).delta(2,2)+i.delta(0,2)+i.delta(1,2)+w.delta(2,2)  +m+p.delta(1,0)+w.delta(2,0)  +o  +o
X2  |  +i.delta(0,0).delta(1,2)+p.delta(0,0).delta(2,2)+i.delta(1,0).delta(1,2)+i.delta(2,0).delta(1,2)+p.delta(1,1).delta(1,2)+p.delta(1,1).delta(2,2)+w.delta(2,1).delta(1,2)+i.delta(0,2)+m.delta(1,2)+w.delta(2,2)  +p.delta(0,0)+m.delta(1,0)+w.delta(2,0)  +m+p.delta(1,1)+w.delta(2,1)  +o
X3  |  +i.delta(0,1).delta(0,2)+p.delta(0,1).delta(2,2)+i.delta(1,1).delta(0,2)+w.delta(1,1).delta(2,2)+i.delta(2,1).delta(0,2)+w.delta(2,1).delta(2,2)+i.delta(1,2)  +o  +p.delta(0,1)+m.delta(1,1)+w.delta(2,1)  +m
INFO (result): CHOICES: [[[0, 1, 2], [0, 1, 2], [2]]]
INFO (result): Total time: 0.0 s (10 ms)
INFO (file_io): saved result in output/notinfinite_3.json
```
</div></div>

#### Matrix

|          |                               `X0`                               |              `X1`               |             `X2`              | `X3` |
|----------|:----------------------------------------------------------------:|:-------------------------------:|:-----------------------------:|:----:|
| **`X0`** |            $m+\infty.\delta(0,2)+\infty.\delta(1,2)$             |               $0$               |              $0$              | $0$  |
|          |                                                                  |                                 |                               |      |
| **`X1`** |          $p.\delta(1,0).\delta(2,2)+\infty.\delta(0,2)$          | $m+p.\delta(1,0)+w.\delta(2,0)$ |              $0$              | $0$  |
|          |               $+\infty.\delta(1,2)+w.\delta(2,2)$                |                                 |                               |
|          |                                                                  |                                 |                               |      |
| **`X2`** |    $\infty.\delta(0,0).\delta(1,2)+p.\delta(0,0).\delta(2,2)$    |  $p.\delta(0,0)+m.\delta(1,0)$  |       $m+p.\delta(1,1)$       | $0$  |
|          | $+\infty.\delta(1,0).\delta(1,2)+\infty.\delta(2,0).\delta(1,2)$ |        $+w.\delta(2,0)$         |       $+w.\delta(2,1)$        |
|          |      $+p.\delta(1,1).\delta(1,2)+p.\delta(1,1).\delta(2,2)$      |                                 |                               |
|          |         $+w.\delta(2,1).\delta(1,2)+\infty.\delta(0,2)$          |                                 |                               |
|          |                  $+m.\delta(1,2)+w.\delta(2,2)$                  |                                 |                               |
|          |                                                                  |                                 |                               |      |
| **`X3`** |    $\infty.\delta(0,1).\delta(0,2)+p.\delta(0,1).\delta(2,2)$    |               $0$               | $p.\delta(0,1)+m.\delta(1,1)$ | $m$  |
|          |   $+\infty.\delta(1,1).\delta(0,2)+w.\delta(1,1).\delta(2,2)$    |                                 |       $+w.\delta(2,1)$        |
|          |   $+\infty.\delta(2,1).\delta(0,2)+w.\delta(2,1).\delta(2,2)$    |                                 |                               |
|          |                      $+\infty.\delta(1,2)$                       |                                 |                               |

Valid choices:

```
[[0, 1, 2], [0, 1, 2], [2]]
```

<details>
<summary>How to read a choice vector</summary>

<pre>

choices:    ↓  ↓  ↓    ↓  ↓  ↓    ↓
          [[0, 1, 2], [0, 1, 2], [2]]
           └───────┘  └───────┘  └─┘
index:         0          1       2

</pre>
</details>


#### Discussion

Compared to previous examples, the matrix is now getting more complicated.
The choice vector tells us that every derivation choice is allowed at indices 0 and 1 . These correspond to the operations inside the `if` statement.
But inside the `while` loop, only choice 2 is allowed to obtain a valid derivation result.
Because there exists a choice for which the program is derivable, this program's variable values growth is bounded by polynomials in their inputs.

