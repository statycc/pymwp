---
title: Challenge Example
subtitle: Try to guess the outcome before determining the result with pymwp. 
last_example: true
---



#### Analyzed Program

```c
void foo(int X0, int X1, int X2){
    if (X0 == 0) {
        X2 = X0 + X1;
    }
    else {
        X2 = X2 + X1;
    }
    X0 = X2 + X1;
    X1 = X0 + X2;
    while(X2 < 10) {
        X2 = X1 + X0;
    }
}
```

After seeing the various preceding examples of programs, with and without polynomial bounds, we present the following challenge.
By inspection, try to determine if this program is polynomially bounded in inputs.
Note that it is unknown whether the `while` loop will terminate, however this is not a problem for determining the result.

**Choose.** The program is...
 
<div class="form-check">
  <input class="form-check-input" type="radio" name="flexRadio" id="P required" required>
  <label class="form-check-label" for="flexRadioDefault1">Polynomially bounded in inputs</label>
</div>
<div class="form-check">
  <input class="form-check-input" type="radio" name="flexRadio" id="Infinite">
  <label class="form-check-label" for="flexRadioDefault2">Infinite</label>
</div>

<br/>

<a class="btn btn-primary" data-bs-toggle="collapse"
href="#solution" role="button" aria-expanded="true"
aria-controls="solution">Reveal Solution</a>


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

### Matrix

Because this matrix is large, we display it in compact form, with
added emphasis on coefficients.

<style>
.table-wrapper tr:not(:first-child) td:not(:first-child) > span.math
    {font-size: 90%;} 
.table-wrapper mjx-mi.mjx-n, .table-wrapper .mjx-i {color: #d63384}
.table-wrapper tr:not(:first-child) td:not(:first-child) > span:not(.math)
    {font-size: 70%;}
.table-wrapper tr:not(:first-child) td 
    {padding-bottom: 20px; vertical-align: top;}
</style>

<div class="table-wrapper">
<table>
<tr>
<td style="width:5%"></td>
<td style="width:25%"><code>X0</code></td>
<td style="width:30%"><code>X1</code></td>
<td style="width:40%"><code>X2</code></td>
</tr>
<tr>
<td><code>X0</code></td>
<td>
  $m$.<span>((0,0)(0,2))</span>
 $+p$.<span>((0,0)(1,2))</span>
 $+w$.<span>((0,0)(2,2))</span>
 $+p$.<span>((1,0)(0,2))</span>
 $+p$.<span>((1,0)(1,2))</span>
 $+p$.<span>((1,0)(2,2))</span>
 $+w$.<span>((2,0)(0,2))</span>
 $+p$.<span>((2,0)(1,2))</span>
 $+w$.<span>((2,0)(2,2))</span></td>
<td>
 $p$.<span>((0,0)(0,2)(1,3))</span>
$+p$.<span>((0,0)(1,2)(1,3))</span>
$+p$.<span>((0,0)(1,2)(2,3))</span>
$+p$.<span>((0,0)(2,2)(1,3))</span>
$+p$.<span>((0,0)(0,3))</span>
$+m$.<span>((0,0)(1,3))</span>
$+w$.<span>((0,0)(2,3))</span>
$+p$.<span>((1,0)(0,3))</span>
$+p$.<span>((1,0)(1,3))</span>
$+p$.<span>((1,0)(2,3))</span>
$+p$.<span>((2,0)(0,2)(1,3))</span>
$+p$.<span>((2,0)(1,2)(1,3))</span>
$+p$.<span>((2,0)(1,2)(2,3))</span>
$+p$.<span>((2,0)(2,2)(1,3))</span>
$+p$.<span>((2,0)(0,3))</span>
$+w$.<span>((2,0)(1,3))</span>
$+w$.<span>((2,0)(2,3))</span>
</td>
<td>
$+m$.<span>((0,0))</span>
$+p$.<span>((0,0)(0,2)(1,3)(2,4))</span>
$+\infty$.<span>((0,0)(0,2)(0,4))</span>
$+w$.<span>((0,0)(0,2)(2,4))</span>
$+\infty$.<span>((0,0)(1,2)(0,4))</span>
$+p$.<span>((0,0)(1,2)(1,4))</span>
$+p$.<span>((0,0)(1,2)(2,4))</span>
$+p$.<span>((0,0)(2,2)(1,3)(2,4))</span>
$+\infty$.<span>((0,0)(2,2)(0,4))</span>
$+w$.<span>((0,0)(2,2)(1,4))</span>
$+w$.<span>((0,0)(2,2)(2,4))</span>
$+p$.<span>((0,0)(0,3)(0,4))</span>
$+\infty$.<span>((0,0)(0,3)(1,4))</span>
$+p$.<span>((0,0)(0,3)(2,4))</span>
$+\infty$.<span>((0,0)(1,3)(1,4))</span>
$+w$.<span>((0,0)(1,3)(2,4))</span>
$+w$.<span>((0,0)(2,3)(0,4))</span>
$+\infty$.<span>((0,0)(2,3)(1,4))</span>
$+w$.<span>((0,0)(2,3)(2,4))</span>
$+p$.<span>((1,0))</span>
$+\infty$.<span>((1,0)(0,2)(0,4))</span>
$+\infty$.<span>((1,0)(1,2)(0,4))</span>
$+\infty$.<span>((1,0)(2,2)(0,4))</span>
$+\infty$.<span>((1,0)(0,3)(1,4))</span>
$+\infty$.<span>((1,0)(1,3)(1,4))</span>
$+\infty$.<span>((1,0)(2,3)(1,4))</span>
$+w$.<span>((2,0))</span>
$+p$.<span>((2,0)(0,2)(1,3)(2,4))</span>
$+\infty$.<span>((2,0)(0,2)(0,4))</span>
$+\infty$.<span>((2,0)(1,2)(0,4))</span>
$+p$.<span>((2,0)(1,2)(1,4))</span>
$+p$.<span>((2,0)(1,2)(2,4))</span>
$+p$.<span>((2,0)(2,2)(1,3)(2,4))</span>
$+\infty$.<span>((2,0)(2,2)(0,4))</span>
$+p$.<span>((2,0)(0,3)(0,4))</span>
$+\infty$.<span>((2,0)(0,3)(1,4))</span>
$+p$.<span>((2,0)(0,3)(2,4))</span>
$+\infty$.<span>((2,0)(1,3)(1,4))</span>
$+\infty$.<span>((2,0)(2,3)(1,4))</span>
</td>
</tr>
<tr><td><code>X1</code></td>
<td>
 $p$.<span>((0,0)(1,2))</span>
$+p$.<span>((0,0)(2,2))</span>
$+p$.<span>((1,0)(1,2))</span>
$+p$.<span>((2,0)(1,2))</span>
$+p$.<span>((0,1)(1,2))</span>
$+p$.<span>((0,1)(2,2))</span>
$+p$.<span>((1,1)(1,2))</span>
$+p$.<span>((2,1)(1,2))</span>
$+p$.<span>((0,2))</span>
$+m$.<span>((1,2))</span>
$+w$.<span>((2,2))</span>
</td>
<td>
$p$.<span>((0,0)(0,3))</span>
$+p$.<span>((0,0)(1,3))</span>
$+p$.<span>((0,0)(2,3))</span>
$+p$.<span>((1,0)(1,2)(2,3))</span>
$+p$.<span>((1,0)(0,3))</span>
$+m$.<span>((1,0)(1,3))</span>
$+w$.<span>((1,0)(2,3))</span>
$+p$.<span>((2,0)(1,2)(2,3))</span>
$+p$.<span>((2,0)(0,3))</span>
$+w$.<span>((2,0)(1,3))</span>
$+w$.<span>((2,0)(2,3))</span>
$+p$.<span>((0,1)(0,3))</span>
$+p$.<span>((0,1)(1,3))</span>
$+p$.<span>((0,1)(2,3))</span>
$+p$.<span>((1,1)(1,2)(2,3))</span>
$+p$.<span>((1,1)(0,3))</span>
$+m$.<span>((1,1)(1,3))</span>
$+w$.<span>((1,1)(2,3))</span>
$+p$.<span>((2,1)(1,2),(2,3))</span>
$+p$.<span>((2,1)(0,3))</span>
$+w$.<span>((2,1)(1,3))</span>
$+w$.<span>((2,1)(2,3))</span>
$+p$.<span>((0,2)(0,3))</span>
$+p$.<span>((0,2)(1,3))</span>
$+p$.<span>((0,2)(2,3))</span>
$+m$.<span>((1,2)(0,3))</span>
$+p$.<span>((1,2)(1,3))</span>
$+w$.<span>((1,2)(2,3))</span>
$+w$.<span>((2,2)(0,3))</span>
$+p$.<span>((2,2)(1,3))</span>
$+w$.<span>((2,2)(2,3))</span>
</td>
<td>
 $p$.<span>((0,0))</span>
$+\infty$.<span>((0,0),(0,3)(1,4))</span>
$+\infty$.<span>((0,0),(1,3),(1,4))</span>
$+\infty$.<span>((0,0),(2,3),(1,4))</span>
$+m$.<span>((1,0))</span>
$+p$.<span>((1,0),(1,2),(1,4))</span>
$+p$.<span>((1,0),(1,2),(2,4))</span>
$+p$.<span>((1,0),(0,3),(0,4))</span>
$+\infty$.<span>((1,0),(0,3),(1,4))</span>
$+p$.<span>((1,0),(0,3),(2,4))</span>
$+\infty$.<span>((1,0),(1,3),(1,4))</span>
$+w$.<span>((1,0),(1,3),(2,4))</span>
$+w$.<span>((1,0),(2,3),(0,4))</span>
$+\infty$.<span>((1,0),(2,3),(1,4))</span>
$+w$.<span>((1,0),(2,3),(2,4))</span>
$+w$.<span>((2,0))</span>
$+p$.<span>((2,0),(1,2),(1,4))</span>
$+p$.<span>((2,0),(1,2),(2,4))</span>
$+p$.<span>((2,0),(0,3),(0,4))</span>
$+\infty$.<span>((2,0),(0,3),(1,4))</span>
$+p$.<span>((2,0),(0,3),(2,4))</span>
$+\infty$.<span>((2,0),(1,3),(1,4))</span>
$+\infty$.<span>((2,0),(2,3),(1,4))</span>
$+p$.<span>((0,1))</span>
$+\infty$.<span>((0,1),(0,3),(1,4))</span>
$+\infty$.<span>((0,1),(1,3),(1,4))</span>
$+\infty$.<span>((0,1),(2,3),(1,4))</span>
$+m$.<span>((1,1))</span>
$+p$.<span>((1,1),(1,2),(1,4))</span>
$+p$.<span>((1,1),(1,2),(2,4))</span>
$+p$.<span>((1,1),(0,3),(0,4))</span>
$+\infty$.<span>((1,1),(0,3),(1,4))</span>
$+p$.<span>((1,1),(0,3),(2,4))</span>
$+\infty$.<span>((1,1),(1,3),(1,4))</span>
$+w$.<span>((1,1),(1,3),(2,4))</span>
$+w$.<span>((1,1),(2,3),(0,4))</span>
$+\infty$.<span>((1,1),(2,3),(1,4))</span>
$+w$.<span>((1,1),(2,3),(2,4))</span>
$+w$.<span>((2,1))</span>
$+p$.<span>((2,1),(1,2),(1,4))</span>
$+p$.<span>((2,1),(1,2),(2,4))</span>
$+p$.<span>((2,1),(0,3),(0,4))</span>
$+\infty$.<span>((2,1),(0,3),(1,4))</span>
$+p$.<span>((2,1),(0,3),(2,4))</span>
$+\infty$.<span>((2,1),(1,3),(1,4))</span>
$+\infty$.<span>((2,1),(2,3),(1,4))</span>
$+\infty$.<span>((0,2),(0,3),(1,4))</span>
$+\infty$.<span>((0,2),(1,3),(1,4))</span>
$+\infty$.<span>((0,2),(2,3),(1,4))</span>
$+\infty$.<span>((0,2),(0,4))</span>
$+p$.<span>((0,2),(1,4))</span>
$+p$.<span>((0,2),(2,4))</span>
$+\infty$.<span>((1,2),(0,3),(1,4))</span>
$+\infty$.<span>((1,2),(1,3),(1,4))</span>
$+p$.<span>((1,2),(1,3),(2,4))</span>
$+\infty$.<span>((1,2),(2,3),(1,4))</span>
$+\infty$.<span>((1,2),(0,4))</span>
$+m$.<span>((1,2),(1,4))</span>
$+w$.<span>((1,2),(2,4))</span>
$+\infty$.<span>((2,2),(0,3),(1,4))</span>
$+\infty$.<span>((2,2),(1,3),(1,4))</span>
$+p$.<span>((2,2),(1,3),(2,4))</span>
$+\infty$.<span>((2,2),(2,3),(1,4))</span>
$+\infty$.<span>((2,2),(0,4))</span>
$+w$.<span>((2,2),(1,4))</span>
$+w$.<span>((2,2),(2,4))</span>
</td></tr>
<tr><td><code>X2</code></td><td>
 $m$.<span>((0,1)(0,2))</span>
$+p$.<span>((0,1)(1,2))</span>
$+w$.<span>((0,1)(2,2))</span>
$+p$.<span>((1,1)(0,2))</span>
$+p$.<span>((1,1)(1,2))</span>
$+p$.<span>((1,1)(2,2))</span>
$+w$.<span>((2,1)(0,2))</span>
$+p$.<span>((2,1)(1,2))</span>
$+w$.<span>((2,1)(2,2))</span>
</td><td>
$p$.<span>((0,1)(0,2)(1,3))</span>
$+p$.<span>((0,1)(1,2)(1,3))</span>
$+p$.<span>((0,1)(1,2)(2,3))</span>
$+p$.<span>((0,1)(2,2)(1,3))</span>
$+p$.<span>((0,1)(0,3))</span>
$+m$.<span>((0,1)(1,3))</span>
$+w$.<span>((0,1)(2,3))</span>
$+p$.<span>((1,1)(0,3))</span>
$+p$.<span>((1,1)(1,3))</span>
$+p$.<span>((1,1)(2,3))</span>
$+p$.<span>((2,1)(0,2)(1,3))</span>
$+p$.<span>((2,1)(1,2)(1,3))</span>
$+p$.<span>((2,1)(1,2)(2,3))</span>
$+p$.<span>((2,1)(2,2)(1,3))</span>
$+p$.<span>((2,1)(0,3))</span>
$+w$.<span>((2,1)(1,3))</span>
$+w$.<span>((2,1)(2,3))</span></td><td>
$m.$<span>((0,1))</span>
$+p.$<span>((0,1)(0,2)(1,3)(2,4))</span>
$+\infty.$<span>((0,1)(0,2)(0,4))</span>
$+w.$<span>((0,1)(0,2)(2,4))</span>
$+\infty.$<span>((0,1)(1,2)(0,4))</span>
$+p.$<span>((0,1)(1,2)(1,4))</span>
$+p.$<span>((0,1)(1,2)(2,4))</span>
$+p.$<span>((0,1)(2,2)(1,3)(2,4))</span>
$+\infty.$<span>((0,1)(2,2)(0,4))</span>
$+w.$<span>((0,1)(2,2)(1,4))</span>
$+w.$<span>((0,1)(2,2)(2,4))</span>
$+p.$<span>((0,1)(0,3)(0,4))</span>
$+\infty.$<span>((0,1)(0,3)(1,4))</span>
$+p.$<span>((0,1)(0,3)(2,4))</span>
$+\infty.$<span>((0,1)(1,3)(1,4))</span>
$+w.$<span>((0,1)(1,3)(2,4))</span>
$+w.$<span>((0,1)(2,3)(0,4))</span>
$+\infty.$<span>((0,1)(2,3)(1,4))</span>
$+w.$<span>((0,1)(2,3)(2,4))</span>
$+p.$<span>((1,1))</span>
$+\infty.$<span>((1,1)(0,2)(0,4))</span>
$+\infty.$<span>((1,1)(1,2)(0,4))</span>
$+\infty.$<span>((1,1)(2,2)(0,4))</span>
$+\infty.$<span>((1,1)(0,3)(1,4))</span>
$+\infty.$<span>((1,1)(1,3)(1,4))</span>
$+\infty.$<span>((1,1)(2,3)(1,4))</span>
$+w.$<span>((2,1))</span>
$+p.$<span>((2,1)(0,2)(1,3)(2,4))</span>
$+\infty.$<span>((2,1)(0,2)(0,4))</span>
$+\infty.$<span>((2,1)(1,2)(0,4))</span>
$+p.$<span>((2,1)(1,2)(1,4))</span>
$+p.$<span>((2,1)(1,2)(2,4))</span>
$+p.$<span>((2,1)(2,2)(1,3)(2,4))</span>
$+\infty.$<span>((2,1)(2,2)(0,4))</span>
$+p.$<span>((2,1)(0,3)(0,4))</span>
$+\infty.$<span>((2,1)(0,3)(1,4))</span>
$+p.$<span>((2,1)(0,3)(2,4))</span>
$+\infty.$<span>((2,1)(1,3)(1,4))</span>
$+\infty.$<span>((2,1)(2,3)(1,4))</span>
</td></tr>
</table>
</div>

Valid choices:

```
[[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [2]]
```

#### Discussion

Variables `X0` and `X1` dependencies are consistently polynomially bounded for all choices.
This is observable in the corresponding columns of the matrix, since they contain no $\infty$ coefficients.

The situation is different for variable `X2`, the rightmost column in the matrix. Multiple derivation choices fail.
From the matrix, and from the choice vector, we can also observe that the critical choice occurs at index 4.
It corresponds to the statement inside the `while` loop. Failure may occur independent of the which branch of the preceding conditional statement was selected.

There are, however, multiple sequences of choices that allow completing the derivation.
The choice vector indicated how to complete the derivation.
For example, choices $[0, 0, 0, 0, 2]$ and $[1, 2, 1, 1, 2]$ are valid.

Because a valid derivation exists, the solution is yes, the program is polynomially bounded in inputs.

</div> 
 