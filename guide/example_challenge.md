---
title: Challenge Example
subtitle: Try to guess the outcome before determining the result with pymwp. 
last_example: true
---



#### Analyzed Program

```c
int foo(int X0, int X1, int X2){
    if (X0) {
        X2 = X0 + X1;
    }
    else {
        X2 = X2 + X1;
    }
    X0 = X2 + X1;
    X1 = X0 + X2;
    while(𝔹) {
        X2 = X1 + X0;
    }
}

```

After seeing the examples of programs with and without polynomial bounds, we present the following challenge.
By inspection, try to determine if this program is polynomially bounded in inputs.
Note that it is unknown whether the `while` loop will terminate, however this is not a problem for determining the result.


<br/>

<p>
  <a class="btn btn-primary" data-bs-toggle="collapse"
    href="#solution" role="button" aria-expanded="false"
    aria-controls="solution">
    Reveal Solution
  </a>
</p>
<div class="collapse" id="solution"> 

#### CLI Command

<details>
<summary>Get this example</summary>

```console
wget https://raw.githubusercontent.com/statycc/pymwp/main/c_files/other/dense_loop.c
```
</details>

```console
pymwp dense_loop.c --fin
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
DEBUG (analysis): variables of foo: ['X0', 'X1', 'X2']
DEBUG (analysis): computing relation...0 of 4
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
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): matrix homogenisation...
DEBUG (analysis): computing composition...0 of 4
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): computing relation...1 of 4
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (analysis): computing composition...1 of 4
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): computing relation...2 of 4
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (analysis): computing composition...2 of 4
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): computing relation...3 of 4
DEBUG (analysis): in compute_relation
DEBUG (analysis): analysing While
DEBUG (analysis): in compute_relation
DEBUG (analysis): Computing Relation (first case / binary op)
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (analysis): while loop fixpoint
DEBUG (relation): computing fixpoint for variables ['X2', 'X1', 'X0']
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): starting composition...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (relation): fixpoint done ['X2', 'X1', 'X0']
DEBUG (analysis): computing composition...3 of 4
DEBUG (relation): starting composition...
DEBUG (relation): matrix homogenisation...
DEBUG (relation): composing matrix product...
DEBUG (relation): ...relation composition done!
DEBUG (choice): infinity paths: [(0, 4)] # [(1, 4)]
DEBUG (choice): maximum distinct vectors: 1
INFO (result): 
MATRIX
X0  |  +m.delta(0,0).delta(0,2)+p.delta(0,0).delta(1,2)+w.delta(0,0).delta(2,2)+p.delta(1,0).delta(0,2)+p.delta(1,0).delta(1,2)+p.delta(1,0).delta(2,2)+w.delta(2,0).delta(0,2)+p.delta(2,0).delta(1,2)+w.delta(2,0).delta(2,2)  +p.delta(0,0).delta(0,2).delta(1,3)+p.delta(0,0).delta(1,2).delta(1,3)+p.delta(0,0).delta(1,2).delta(2,3)+p.delta(0,0).delta(2,2).delta(1,3)+p.delta(0,0).delta(0,3)+m.delta(0,0).delta(1,3)+w.delta(0,0).delta(2,3)+p.delta(1,0).delta(0,3)+p.delta(1,0).delta(1,3)+p.delta(1,0).delta(2,3)+p.delta(2,0).delta(0,2).delta(1,3)+p.delta(2,0).delta(1,2).delta(1,3)+p.delta(2,0).delta(1,2).delta(2,3)+p.delta(2,0).delta(2,2).delta(1,3)+p.delta(2,0).delta(0,3)+w.delta(2,0).delta(1,3)+w.delta(2,0).delta(2,3)  +m.delta(0,0)+p.delta(0,0).delta(0,2).delta(1,3).delta(2,4)+i.delta(0,0).delta(0,2).delta(0,4)+w.delta(0,0).delta(0,2).delta(2,4)+i.delta(0,0).delta(1,2).delta(0,4)+p.delta(0,0).delta(1,2).delta(1,4)+p.delta(0,0).delta(1,2).delta(2,4)+p.delta(0,0).delta(2,2).delta(1,3).delta(2,4)+i.delta(0,0).delta(2,2).delta(0,4)+w.delta(0,0).delta(2,2).delta(1,4)+w.delta(0,0).delta(2,2).delta(2,4)+p.delta(0,0).delta(0,3).delta(0,4)+i.delta(0,0).delta(0,3).delta(1,4)+p.delta(0,0).delta(0,3).delta(2,4)+i.delta(0,0).delta(1,3).delta(1,4)+w.delta(0,0).delta(1,3).delta(2,4)+w.delta(0,0).delta(2,3).delta(0,4)+i.delta(0,0).delta(2,3).delta(1,4)+w.delta(0,0).delta(2,3).delta(2,4)+p.delta(1,0)+i.delta(1,0).delta(0,2).delta(0,4)+i.delta(1,0).delta(1,2).delta(0,4)+i.delta(1,0).delta(2,2).delta(0,4)+i.delta(1,0).delta(0,3).delta(1,4)+i.delta(1,0).delta(1,3).delta(1,4)+i.delta(1,0).delta(2,3).delta(1,4)+w.delta(2,0)+p.delta(2,0).delta(0,2).delta(1,3).delta(2,4)+i.delta(2,0).delta(0,2).delta(0,4)+i.delta(2,0).delta(1,2).delta(0,4)+p.delta(2,0).delta(1,2).delta(1,4)+p.delta(2,0).delta(1,2).delta(2,4)+p.delta(2,0).delta(2,2).delta(1,3).delta(2,4)+i.delta(2,0).delta(2,2).delta(0,4)+p.delta(2,0).delta(0,3).delta(0,4)+i.delta(2,0).delta(0,3).delta(1,4)+p.delta(2,0).delta(0,3).delta(2,4)+i.delta(2,0).delta(1,3).delta(1,4)+i.delta(2,0).delta(2,3).delta(1,4)
X1  |  +p.delta(0,0).delta(1,2)+p.delta(0,0).delta(2,2)+p.delta(1,0).delta(1,2)+p.delta(2,0).delta(1,2)+p.delta(0,1).delta(1,2)+p.delta(0,1).delta(2,2)+p.delta(1,1).delta(1,2)+p.delta(2,1).delta(1,2)+p.delta(0,2)+m.delta(1,2)+w.delta(2,2)  +p.delta(0,0).delta(0,3)+p.delta(0,0).delta(1,3)+p.delta(0,0).delta(2,3)+p.delta(1,0).delta(1,2).delta(2,3)+p.delta(1,0).delta(0,3)+m.delta(1,0).delta(1,3)+w.delta(1,0).delta(2,3)+p.delta(2,0).delta(1,2).delta(2,3)+p.delta(2,0).delta(0,3)+w.delta(2,0).delta(1,3)+w.delta(2,0).delta(2,3)+p.delta(0,1).delta(0,3)+p.delta(0,1).delta(1,3)+p.delta(0,1).delta(2,3)+p.delta(1,1).delta(1,2).delta(2,3)+p.delta(1,1).delta(0,3)+m.delta(1,1).delta(1,3)+w.delta(1,1).delta(2,3)+p.delta(2,1).delta(1,2).delta(2,3)+p.delta(2,1).delta(0,3)+w.delta(2,1).delta(1,3)+w.delta(2,1).delta(2,3)+p.delta(0,2).delta(0,3)+p.delta(0,2).delta(1,3)+p.delta(0,2).delta(2,3)+m.delta(1,2).delta(0,3)+p.delta(1,2).delta(1,3)+w.delta(1,2).delta(2,3)+w.delta(2,2).delta(0,3)+p.delta(2,2).delta(1,3)+w.delta(2,2).delta(2,3)  +p.delta(0,0)+i.delta(0,0).delta(0,3).delta(1,4)+i.delta(0,0).delta(1,3).delta(1,4)+i.delta(0,0).delta(2,3).delta(1,4)+m.delta(1,0)+p.delta(1,0).delta(1,2).delta(1,4)+p.delta(1,0).delta(1,2).delta(2,4)+p.delta(1,0).delta(0,3).delta(0,4)+i.delta(1,0).delta(0,3).delta(1,4)+p.delta(1,0).delta(0,3).delta(2,4)+i.delta(1,0).delta(1,3).delta(1,4)+w.delta(1,0).delta(1,3).delta(2,4)+w.delta(1,0).delta(2,3).delta(0,4)+i.delta(1,0).delta(2,3).delta(1,4)+w.delta(1,0).delta(2,3).delta(2,4)+w.delta(2,0)+p.delta(2,0).delta(1,2).delta(1,4)+p.delta(2,0).delta(1,2).delta(2,4)+p.delta(2,0).delta(0,3).delta(0,4)+i.delta(2,0).delta(0,3).delta(1,4)+p.delta(2,0).delta(0,3).delta(2,4)+i.delta(2,0).delta(1,3).delta(1,4)+i.delta(2,0).delta(2,3).delta(1,4)+p.delta(0,1)+i.delta(0,1).delta(0,3).delta(1,4)+i.delta(0,1).delta(1,3).delta(1,4)+i.delta(0,1).delta(2,3).delta(1,4)+m.delta(1,1)+p.delta(1,1).delta(1,2).delta(1,4)+p.delta(1,1).delta(1,2).delta(2,4)+p.delta(1,1).delta(0,3).delta(0,4)+i.delta(1,1).delta(0,3).delta(1,4)+p.delta(1,1).delta(0,3).delta(2,4)+i.delta(1,1).delta(1,3).delta(1,4)+w.delta(1,1).delta(1,3).delta(2,4)+w.delta(1,1).delta(2,3).delta(0,4)+i.delta(1,1).delta(2,3).delta(1,4)+w.delta(1,1).delta(2,3).delta(2,4)+w.delta(2,1)+p.delta(2,1).delta(1,2).delta(1,4)+p.delta(2,1).delta(1,2).delta(2,4)+p.delta(2,1).delta(0,3).delta(0,4)+i.delta(2,1).delta(0,3).delta(1,4)+p.delta(2,1).delta(0,3).delta(2,4)+i.delta(2,1).delta(1,3).delta(1,4)+i.delta(2,1).delta(2,3).delta(1,4)+i.delta(0,2).delta(0,3).delta(1,4)+i.delta(0,2).delta(1,3).delta(1,4)+i.delta(0,2).delta(2,3).delta(1,4)+i.delta(0,2).delta(0,4)+p.delta(0,2).delta(1,4)+p.delta(0,2).delta(2,4)+i.delta(1,2).delta(0,3).delta(1,4)+i.delta(1,2).delta(1,3).delta(1,4)+p.delta(1,2).delta(1,3).delta(2,4)+i.delta(1,2).delta(2,3).delta(1,4)+i.delta(1,2).delta(0,4)+m.delta(1,2).delta(1,4)+w.delta(1,2).delta(2,4)+i.delta(2,2).delta(0,3).delta(1,4)+i.delta(2,2).delta(1,3).delta(1,4)+p.delta(2,2).delta(1,3).delta(2,4)+i.delta(2,2).delta(2,3).delta(1,4)+i.delta(2,2).delta(0,4)+w.delta(2,2).delta(1,4)+w.delta(2,2).delta(2,4)
X2  |  +m.delta(0,1).delta(0,2)+p.delta(0,1).delta(1,2)+w.delta(0,1).delta(2,2)+p.delta(1,1).delta(0,2)+p.delta(1,1).delta(1,2)+p.delta(1,1).delta(2,2)+w.delta(2,1).delta(0,2)+p.delta(2,1).delta(1,2)+w.delta(2,1).delta(2,2)  +p.delta(0,1).delta(0,2).delta(1,3)+p.delta(0,1).delta(1,2).delta(1,3)+p.delta(0,1).delta(1,2).delta(2,3)+p.delta(0,1).delta(2,2).delta(1,3)+p.delta(0,1).delta(0,3)+m.delta(0,1).delta(1,3)+w.delta(0,1).delta(2,3)+p.delta(1,1).delta(0,3)+p.delta(1,1).delta(1,3)+p.delta(1,1).delta(2,3)+p.delta(2,1).delta(0,2).delta(1,3)+p.delta(2,1).delta(1,2).delta(1,3)+p.delta(2,1).delta(1,2).delta(2,3)+p.delta(2,1).delta(2,2).delta(1,3)+p.delta(2,1).delta(0,3)+w.delta(2,1).delta(1,3)+w.delta(2,1).delta(2,3)  +m.delta(0,1)+p.delta(0,1).delta(0,2).delta(1,3).delta(2,4)+i.delta(0,1).delta(0,2).delta(0,4)+w.delta(0,1).delta(0,2).delta(2,4)+i.delta(0,1).delta(1,2).delta(0,4)+p.delta(0,1).delta(1,2).delta(1,4)+p.delta(0,1).delta(1,2).delta(2,4)+p.delta(0,1).delta(2,2).delta(1,3).delta(2,4)+i.delta(0,1).delta(2,2).delta(0,4)+w.delta(0,1).delta(2,2).delta(1,4)+w.delta(0,1).delta(2,2).delta(2,4)+p.delta(0,1).delta(0,3).delta(0,4)+i.delta(0,1).delta(0,3).delta(1,4)+p.delta(0,1).delta(0,3).delta(2,4)+i.delta(0,1).delta(1,3).delta(1,4)+w.delta(0,1).delta(1,3).delta(2,4)+w.delta(0,1).delta(2,3).delta(0,4)+i.delta(0,1).delta(2,3).delta(1,4)+w.delta(0,1).delta(2,3).delta(2,4)+p.delta(1,1)+i.delta(1,1).delta(0,2).delta(0,4)+i.delta(1,1).delta(1,2).delta(0,4)+i.delta(1,1).delta(2,2).delta(0,4)+i.delta(1,1).delta(0,3).delta(1,4)+i.delta(1,1).delta(1,3).delta(1,4)+i.delta(1,1).delta(2,3).delta(1,4)+w.delta(2,1)+p.delta(2,1).delta(0,2).delta(1,3).delta(2,4)+i.delta(2,1).delta(0,2).delta(0,4)+i.delta(2,1).delta(1,2).delta(0,4)+p.delta(2,1).delta(1,2).delta(1,4)+p.delta(2,1).delta(1,2).delta(2,4)+p.delta(2,1).delta(2,2).delta(1,3).delta(2,4)+i.delta(2,1).delta(2,2).delta(0,4)+p.delta(2,1).delta(0,3).delta(0,4)+i.delta(2,1).delta(0,3).delta(1,4)+p.delta(2,1).delta(0,3).delta(2,4)+i.delta(2,1).delta(1,3).delta(1,4)+i.delta(2,1).delta(2,3).delta(1,4)
INFO (result): CHOICES: [[[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [2]]]
INFO (result): Total time: 0.1 s (79 ms)
INFO (file_io): saved result in output/dense_loop.json
```
</div></div>


#### Matrix

|          |             `X0`              |                                             `X1`                                             | `X2`                                                                                              |
|----------|:-----------------------------:|:--------------------------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------------|
| **`X0`** |  $m.\delta(0,0).\delta(0,2)$  |        $p.\delta(0,0).\delta(0,2).\delta(1,3)+p.\delta(0,0).\delta(1,2).\delta(1,3)$         | $m.\delta(0,0)+p.\delta(0,0).\delta(0,2).\delta(1,3).\delta(2,4)$                                 |
|          | $+p.\delta(0,0).\delta(1,2)$  |        $+p.\delta(0,0).\delta(1,2).\delta(2,3)+p.\delta(0,0).\delta(2,2).\delta(1,3)$        | $+\infty.\delta(0,0).\delta(0,2).\delta(0,4)+w.\delta(0,0).\delta(0,2).\delta(2,4)$               |
|          | $+w.\delta(0,0).\delta(2,2)$  |       $+p.\delta(0,0).\delta(0,3)+m.\delta(0,0).\delta(1,3)+w.\delta(0,0).\delta(2,3)$       | $+\infty.\delta(0,0).\delta(1,2).\delta(0,4)+p.\delta(0,0).\delta(1,2).\delta(1,4)$               |
|          | $+p.\delta(1,0).\delta(0,2)$  |       $+p.\delta(1,0).\delta(0,3)+p.\delta(1,0).\delta(1,3)+p.\delta(1,0).\delta(2,3)$       | $+p.\delta(0,0).\delta(1,2).\delta(2,4)+p.\delta(0,0).\delta(2,2).\delta(1,3).\delta(2,4)$        |
|          | $+p.\delta(1,0).\delta(1,2)$  |        $+p.\delta(2,0).\delta(0,2).\delta(1,3)+p.\delta(2,0).\delta(1,2).\delta(1,3)$        | $+\infty.\delta(0,0).\delta(2,2).\delta(0,4)+w.\delta(0,0).\delta(2,2).\delta(1,4)$               |
|          | $+p.\delta(1,0).\delta(2,2)$  |        $+p.\delta(2,0).\delta(1,2).\delta(2,3)+p.\delta(2,0).\delta(2,2).\delta(1,3)$        | $+w.\delta(0,0).\delta(2,2).\delta(2,4)+p.\delta(0,0).\delta(0,3).\delta(0,4)$                    |
|          | $+w.\delta(2,0).\delta(0,2)$  |       $+p.\delta(2,0).\delta(0,3)+w.\delta(2,0).\delta(1,3)+w.\delta(2,0).\delta(2,3)$       | $+\infty.\delta(0,0).\delta(0,3).\delta(1,4)+p.\delta(0,0).\delta(0,3).\delta(2,4)$               |
|          | $+p.\delta(2,0).\delta(1,2)$  |                                                                                              | $+\infty.\delta(0,0).\delta(1,3).\delta(1,4)+w.\delta(0,0).\delta(1,3).\delta(2,4)$               |
|          | $+w.\delta(2,0).\delta(2,2)$  |                                                                                              | $+w.\delta(0,0).\delta(2,3).\delta(0,4)+\infty.\delta(0,0).\delta(2,3).\delta(1,4)$               |
|          |                               |                                                                                              | $+w.\delta(0,0).\delta(2,3).\delta(2,4)+p.\delta(1,0)+\infty.\delta(1,0).\delta(0,2).\delta(0,4)$ |
|          |                               |                                                                                              | $+\infty.\delta(1,0).\delta(1,2).\delta(0,4)+\infty.\delta(1,0).\delta(2,2).\delta(0,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(1,0).\delta(0,3).\delta(1,4)+\infty.\delta(1,0).\delta(1,3).\delta(1,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(1,0).\delta(2,3).\delta(1,4)+w.\delta(2,0)$                                       |
|          |                               |                                                                                              | $+p.\delta(2,0).\delta(0,2).\delta(1,3).\delta(2,4)+\infty.\delta(2,0).\delta(0,2).\delta(0,4)$   |
|          |                               |                                                                                              | $+\infty.\delta(2,0).\delta(1,2).\delta(0,4)+p.\delta(2,0).\delta(1,2).\delta(1,4)$               |
|          |                               |                                                                                              | $+p.\delta(2,0).\delta(1,2).\delta(2,4)+p.\delta(2,0).\delta(2,2).\delta(1,3).\delta(2,4)$        |
|          |                               |                                                                                              | $+\infty.\delta(2,0).\delta(2,2).\delta(0,4)+p.\delta(2,0).\delta(0,3).\delta(0,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(2,0).\delta(0,3).\delta(1,4)+p.\delta(2,0).\delta(0,3).\delta(2,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(2,0).\delta(1,3).\delta(1,4)+\infty.\delta(2,0).\delta(2,3).\delta(1,4)$          |
|          |                               |                                                                                              |                                                                                                   |
| **`X1`** |  $p.\delta(0,0).\delta(1,2)$  |       $p.\delta(0,0).\delta(0,3)+p.\delta(0,0).\delta(1,3)+p.\delta(0,0).\delta(2,3)$        | $p.\delta(0,0)+\infty.\delta(0,0).\delta(0,3).\delta(1,4)$                                        |
|          | $+p.\delta(0,0).\delta(2,2)$  |              $+p.\delta(1,0).\delta(1,2).\delta(2,3)+p.\delta(1,0).\delta(0,3)$              | $+\infty.\delta(0,0).\delta(1,3).\delta(1,4)+\infty.\delta(0,0).\delta(2,3).\delta(1,4)$          |
|          | $+p.\delta(1,0).\delta(1,2)$  |                    $+m.\delta(1,0).\delta(1,3)+w.\delta(1,0).\delta(2,3)$                    | $+m.\delta(1,0)+p.\delta(1,0).\delta(1,2).\delta(1,4)+p.\delta(1,0).\delta(1,2).\delta(2,4)$      |
|          | $+p.\delta(2,0).\delta(1,2)$  |              $+p.\delta(2,0).\delta(1,2).\delta(2,3)+p.\delta(2,0).\delta(0,3)$              | $+p.\delta(1,0).\delta(0,3).\delta(0,4)+\infty.\delta(1,0).\delta(0,3).\delta(1,4)$               |
|          | $+p.\delta(0,1).\delta(1,2)$  |       $+w.\delta(2,0).\delta(1,3)+w.\delta(2,0).\delta(2,3)+p.\delta(0,1).\delta(0,3)$       | $+p.\delta(1,0).\delta(0,3).\delta(2,4)+\infty.\delta(1,0).\delta(1,3).\delta(1,4)$               |
|          | $+p.\delta(0,1).\delta(2,2)$  |                    $p.\delta(0,1).\delta(1,3)+p.\delta(0,1).\delta(2,3)$                     | $+w.\delta(1,0).\delta(1,3).\delta(2,4)+w.\delta(1,0).\delta(2,3).\delta(0,4)$                    |
|          | $+p.\delta(1,1).\delta(1,2)$  |              $+p.\delta(1,1).\delta(1,2).\delta(2,3)+p.\delta(1,1).\delta(0,3)$              | $+\infty.\delta(1,0).\delta(2,3).\delta(1,4)+w.\delta(1,0).\delta(2,3).\delta(2,4)$               |
|          | $+p.\delta(2,1).\delta(1,2)$  | $+m.\delta(1,1).\delta(1,3)+w.\delta(1,1).\delta(2,3)+p.\delta(2,1).\delta(1,2).\delta(2,3)$ | $+w.\delta(2,0)+p.\delta(2,0).\delta(1,2).\delta(1,4)+p.\delta(2,0).\delta(1,2).\delta(2,4)$      |
|          |       $+p.\delta(0,2)$        |       $+p.\delta(2,1).\delta(0,3)+w.\delta(2,1).\delta(1,3)+w.\delta(2,1).\delta(2,3)$       | $+p.\delta(2,0).\delta(0,3).\delta(0,4)+\infty.\delta(2,0).\delta(0,3).\delta(1,4)$               |
|          |       $+m.\delta(1,2)$        |       $+p.\delta(0,2).\delta(0,3)+p.\delta(0,2).\delta(1,3)+p.\delta(0,2).\delta(2,3)$       | $+p.\delta(2,0).\delta(0,3).\delta(2,4)+\infty.\delta(2,0).\delta(1,3).\delta(1,4)$               |
|          |       $+w.\delta(2,2)$        |       $+m.\delta(1,2).\delta(0,3)+p.\delta(1,2).\delta(1,3)+w.\delta(1,2).\delta(2,3)$       | $+\infty.\delta(2,0).\delta(2,3).\delta(1,4)+p.\delta(0,1)$                                       |
|          |                               |       $+w.\delta(2,2).\delta(0,3)+p.\delta(2,2).\delta(1,3)+w.\delta(2,2).\delta(2,3)$       | $+\infty.\delta(0,1).\delta(0,3).\delta(1,4)+\infty.\delta(0,1).\delta(1,3).\delta(1,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(0,1).\delta(2,3).\delta(1,4)+m.\delta(1,1)+p.\delta(1,1).\delta(1,2).\delta(1,4)$ |
|          |                               |                                                                                              | $+p.\delta(1,1).\delta(1,2).\delta(2,4)+p.\delta(1,1).\delta(0,3).\delta(0,4)+$                   |
|          |                               |                                                                                              | $+\infty.\delta(1,1).\delta(0,3).\delta(1,4)+p.\delta(1,1).\delta(0,3).\delta(2,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(1,1).\delta(1,3).\delta(1,4)+w.\delta(1,1).\delta(1,3).\delta(2,4)$               |
|          |                               |                                                                                              | $+w.\delta(1,1).\delta(2,3).\delta(0,4)+\infty.\delta(1,1).\delta(2,3).\delta(1,4)$               |
|          |                               |                                                                                              | $+w.\delta(1,1).\delta(2,3).\delta(2,4)+w.\delta(2,1)+p.\delta(2,1).\delta(1,2).\delta(1,4)+$     |
|          |                               |                                                                                              | $+p.\delta(2,1).\delta(1,2).\delta(2,4)+p.\delta(2,1).\delta(0,3).\delta(0,4)$                    |
|          |                               |                                                                                              | $+\infty.\delta(2,1).\delta(0,3).\delta(1,4)+p.\delta(2,1).\delta(0,3).\delta(2,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(2,1).\delta(1,3).\delta(1,4)+\infty.\delta(2,1).\delta(2,3).\delta(1,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(0,2).\delta(0,3).\delta(1,4)+\infty.\delta(0,2).\delta(1,3).\delta(1,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(0,2).\delta(2,3).\delta(1,4)+\infty.\delta(0,2).\delta(0,4)$                      |
|          |                               |                                                                                              | $+p.\delta(0,2).\delta(1,4)+p.\delta(0,2).\delta(2,4)+\infty.\delta(1,2).\delta(0,3).\delta(1,4)$ |
|          |                               |                                                                                              | $+\infty.\delta(1,2).\delta(1,3).\delta(1,4)+p.\delta(1,2).\delta(1,3).\delta(2,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(1,2).\delta(2,3).\delta(1,4)+\infty.\delta(1,2).\delta(0,4)$                      |
|          |                               |                                                                                              | $+m.\delta(1,2).\delta(1,4)+w.\delta(1,2).\delta(2,4)+\infty.\delta(2,2).\delta(0,3).\delta(1,4)$ |
|          |                               |                                                                                              | $+\infty.\delta(2,2).\delta(1,3).\delta(1,4)+p.\delta(2,2).\delta(1,3).\delta(2,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(2,2).\delta(2,3).\delta(1,4)+\infty.\delta(2,2).\delta(0,4)$                      |
|          |                               |                                                                                              | $+w.\delta(2,2).\delta(1,4)+w.\delta(2,2).\delta(2,4)$                                            |
|          |                               |                                                                                              |                                                                                                   |
| **`X2`** |  $m.\delta(0,1).\delta(0,2)$  |        $p.\delta(0,1).\delta(0,2).\delta(1,3)+p.\delta(0,1).\delta(1,2).\delta(1,3)$         | $m.\delta(0,1)+p.\delta(0,1).\delta(0,2).\delta(1,3).\delta(2,4)$                                 |
|          | $+p.\delta(0,1).\delta(1,2)$  |        $+p.\delta(0,1).\delta(1,2).\delta(2,3)+p.\delta(0,1).\delta(2,2).\delta(1,3)$        | $+\infty.\delta(0,1).\delta(0,2).\delta(0,4)+w.\delta(0,1).\delta(0,2).\delta(2,4)$               |
|          | $+w.\delta(0,1).\delta(2,2)$  |       $+p.\delta(0,1).\delta(0,3)+m.\delta(0,1).\delta(1,3)+w.\delta(0,1).\delta(2,3)$       | $+\infty.\delta(0,1).\delta(1,2).\delta(0,4)+p.\delta(0,1).\delta(1,2).\delta(1,4)$               |
|          | $+p.\delta(1,1).\delta(0,2)$  |       $+p.\delta(1,1).\delta(0,3)+p.\delta(1,1).\delta(1,3)+p.\delta(1,1).\delta(2,3)$       | $+p.\delta(0,1).\delta(1,2).\delta(2,4)+p.\delta(0,1).\delta(2,2).\delta(1,3).\delta(2,4)$        |
|          | $+p.\delta(1,1).\delta(1,2)$  |        $+p.\delta(2,1).\delta(0,2).\delta(1,3)+p.\delta(2,1).\delta(1,2).\delta(1,3)$        | $+\infty.\delta(0,1).\delta(2,2).\delta(0,4)+w.\delta(0,1).\delta(2,2).\delta(1,4)$               |
|          | $+p.\delta(1,1).\delta(2,2)$  |        $+p.\delta(2,1).\delta(1,2).\delta(2,3)+p.\delta(2,1).\delta(2,2).\delta(1,3)$        | $+w.\delta(0,1).\delta(2,2).\delta(2,4)+p.\delta(0,1).\delta(0,3).\delta(0,4)$                    |
|          | $+w.\delta(2,1).\delta(0,2)$  |       $+p.\delta(2,1).\delta(0,3)+w.\delta(2,1).\delta(1,3)+w.\delta(2,1).\delta(2,3)$       | $+\infty.\delta(0,1).\delta(0,3).\delta(1,4)+p.\delta(0,1).\delta(0,3).\delta(2,4)$               |
|          | $+p.\delta(2,1).\delta(1,2)$  |                                                                                              | $+\infty.\delta(0,1).\delta(1,3).\delta(1,4)+w.\delta(0,1).\delta(1,3).\delta(2,4)$               |
|          | $+w.\delta(2,1).\delta(2,2)$  |                                                                                              | $+w.\delta(0,1).\delta(2,3).\delta(0,4)+\infty.\delta(0,1).\delta(2,3).\delta(1,4)$               |
|          |                               |                                                                                              | $+w.\delta(0,1).\delta(2,3).\delta(2,4)+p.\delta(1,1)$                                            |
|          |                               |                                                                                              | $+\infty.\delta(1,1).\delta(0,2).\delta(0,4)+\infty.\delta(1,1).\delta(1,2).\delta(0,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(1,1).\delta(2,2).\delta(0,4)+\infty.\delta(1,1).\delta(0,3).\delta(1,4)$          |
|          |                               |                                                                                              | $+\infty.\delta(1,1).\delta(1,3).\delta(1,4)+\infty.\delta(1,1).\delta(2,3).\delta(1,4)$          |
|          |                               |                                                                                              | $+w.\delta(2,1)+p.\delta(2,1).\delta(0,2).\delta(1,3).\delta(2,4)$                                |
|          |                               |                                                                                              | $+\infty.\delta(2,1).\delta(0,2).\delta(0,4)+\infty.\delta(2,1).\delta(1,2).\delta(0,4)$          |
|          |                               |                                                                                              | $+p.\delta(2,1).\delta(1,2).\delta(1,4)+p.\delta(2,1).\delta(1,2).\delta(2,4)$                    |
|          |                               |                                                                                              | $+p.\delta(2,1).\delta(2,2).\delta(1,3).\delta(2,4)+\infty.\delta(2,1).\delta(2,2).\delta(0,4)$   |
|          |                               |                                                                                              | $+p.\delta(2,1).\delta(0,3).\delta(0,4)+\infty.\delta(2,1).\delta(0,3).\delta(1,4)$               |
|          |                               |                                                                                              | $+p.\delta(2,1).\delta(0,3).\delta(2,4)+\infty.\delta(2,1).\delta(1,3).\delta(1,4)$               |
|          |                               |                                                                                              | $+\infty.\delta(2,1).\delta(2,3).\delta(1,4)$                                                     |

Valid choices:

```
[[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [2]]
```

#### Discussion

For any source variable, where either `X0` or `X1` is the target, the dependencies are consistently polynomially bounded, for all choices.
The situation is different between any source variable and `X2` as the target. Multiple deviation choices fail.
From the matrix, we can also observe that failures occur at the `while` loop, independent of the which branch of the conditional statement was selected.

There are however multiple sequences of choices that still allow completing the derivation.
The generated choice vector captures the valid choices we can apply to complete the derivation.
Therefore, the solution is yes, the program is polynomially bounded in inputs.

</div> 
 