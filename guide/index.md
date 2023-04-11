---
title: pymwp
next: Setup
next_href: setup.html
---

pymwp ("paɪ m-w-p") is a tool for automatically performing 
<a href="https://en.wikipedia.org/wiki/Static_program_analysis" target="blank" rel="nofollow noreferrer">static analysis</a> 
on programs written in a subset of the C language.
It analyzes resource usage and determines if a program variables' growth rates are no more than polynomially related to their inputs sizes.

The mathematical foundation of the analyzer is described in paper ["mwp-Analysis Improvement and Implementation: Realizing Implicit Computational Complexity"](https://drops.dagstuhl.de/opus/volltexte/2022/16307/pdf/LIPIcs-FSCD-2022-26.pdf).
The technique is inspired by [_"A Flow Calculus of mwp-Bounds for Complexity Analysis"_](https://doi.org/10.1145/1555746.1555752).

This guide explains pymwp usage and behavior through several high-level examples.

The Main Question
---

For program $P$, <!-- using P here to not confuse with C language -->
the goal of the analyzer is to discover a polynomially bounded data-flow relation, 
between its initial values $x_1,...,x_n$ and final value $x_1^\prime,...,x_n^\prime$.

For an imperative program, this property of interest can be framed as follows.  

```c
void main(int X1, int X2, int X3){ 
   // initial values  ↑

   /*  
    * do calculations involving 
    * variables X1, X2, X3 
    */

   // X1', X2', X3' (final values) 
}
```

Question: $\forall i$, is $\texttt{X}_i \rightsquigarrow \texttt{X}_i^\prime$ polynomially bounded in inputs? 

### Interpreting Matrices

The analysis is performed by applying inference rules to commands of $P$.
These inference rules assign matrices to commands. 
Final matrix $M$ for program $P$ is obtained by compositional analysis of its commands.

After analysis, the matrix $P: M$ contains coefficients representing _dependencies_ between program variables.
These are denoted with coefficients $0, m, w, p$ and $\infty$. 

<details>
<summary>Brief explanation of coefficients</summary>
<div class="card card-body">
The coefficients characterize how data flows between variables.   

* $0$ --- no dependency
* $m$ --- maximal (of linear)
* $w$ --- weak polynomial
* $p$ --- polynomial
* $\infty$ --- infinite (failure)

Ordering of coefficients:  $0 < m < w < p < \infty$.  

In pymwp, `o` is used for $0$ and `i` for $\infty$.
</div>
</details>

One way to think about $\infty$ is derivation failure. Alternatively, obtaining an $\infty$-free result
implies existence of a polynomial growth bound, i.e., the program has the property of interest, or simply "success".


#### Example 1

For some programs the analysis is straightforward.   

<div class="container text-left"><div class="row"><div class="col col-md-4">
PROGRAM

```c
void foo(int x, int y){
  if (x < y) {
    y = x;
  }
}
```

</div><div class="col">

MATRIX

|         | `x` | `y` |
|---------|:---:|:---:|
| **`x`** | $m$ | $m$ |
| **`y`** | $0$ | $m$ | 

</div></div></div>

This obtained matrix contains only 4 simple-value coefficients.
This result indicates that value growth of variables `x` and `y` is polynomially bounded in their inputs.

The result should be read along a vertical column, where the top-row variable is the data flow target, and
the first column gives the data flow source. 

#### Example 2

For more complicated programs, the inference procedure introduces derivation _choice_. 
This is represented in a matrix by complex polynomials.

Variables have different dependencies for different derivation choices.
We capture this in the matrix in form of ordered list of _deltas_, and an associated coefficient.
In other words, by making the derivation choices indicated by a list of deltas, we obtain the associated coefficient.


Deltas are coded as pairs of $(i, j)$ with $i$ the value and $j$ the index in the domain.
Possible values of $i$ are $\{0,1,2\}$. Index $j$ is of type $\mathbb{N}$ and corresponds to a program point where a choice is made.

<div class="container text-left"><div class="row"><div class="col col-md-4">
PROGRAM

```c
void foo(int x, int y){
  while (x < y) {
    x = y + y;
  }
}
```

</div><div class="col">

MATRIX

|         |                            `x`                            | `y` |
|---------|:---------------------------------------------------------:|:---:|
| **`x`** |       $m + \infty.\delta(0,0) + \infty.\delta(1,0)$       | $0$ |
| **`y`** | $\infty.\delta(0,0) + \infty.\delta(1,0) + w.\delta(2,0)$ | $m$ |

</div></div></div>


Variable `x` has different dependencies -- consider pairs (`x`,`x`) and  (`x`,`y`) -- with some choices yielding $\infty$.
In fact, the single matrix compactly captures three possible derivation outcomes:
 
<div class="d-flex flex-wrap flex-row justify-content-left"><div class="p-2">
Choice $(0,0)$

|         |   `x`    | `y` |
|---------|:--------:|:---:|
| **`x`** | $\infty$ | $0$ |
| **`y`** | $\infty$ | $m$ |

</div><div class="p-2"></div><div class="p-2">
Choice $(1,0)$

|         |   `x`    | `y` |
|---------|:--------:|:---:|
| **`x`** | $\infty$ | $0$ |
| **`y`** | $\infty$ | $m$ |

</div><div class="p-2"></div><div class="p-2">
Choice $(2,0)$

|         | `x` | `y` |
|---------|:---:|:---:|
| **`x`** | $m$ | $0$ |
| **`y`** | $w$ | $m$ |

</div></div>


Only the choice $(2,0)$ produces a valid derivation because it does not contain $\infty$ coefficients.

### Analysis Result

A program is derivable when it can be assigned a matrix (of choice) without infinite coefficients.
The soundness theorem of the calculus guarantees that if some choice exists 
that produces an $\infty$-free simple valued matrix, the program variables' value growth is polynomially bounded in inputs.


Program fails the analysis if it is assigned a matrix that always contains infinite coefficients, no matter the choices.
Then it is not possible to establish polynomial growth bound. For these programs, pymwp reports $\infty$ result.


