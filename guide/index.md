---
title: pymwp
next: Setup
next_href: setup.html
---

pymwp ("paɪ m-w-p") is a tool for automatically performing [static analysis](https://en.wikipedia.org/wiki/Static_program_analysis) on programs written in C language. 
It analyzes resource usage and determines if a program variables' growth rates are no more than polynomially related to their inputs sizes.

The mathematical foundation of the analyzer is described in paper ["mwp-Analysis Improvement and Implementation: Realizing Implicit Computational Complexity"](https://drops.dagstuhl.de/opus/volltexte/2022/16307/pdf/LIPIcs-FSCD-2022-26.pdf).
The technique is inspired by [_"A Flow Calculus of mwp-Bounds for Complexity Analysis"_](https://doi.org/10.1145/1555746.1555752).

This guide explains pymwp usage and behavior through several illustrative high-level examples.

The Main Question
---

For program $P$, <!-- using P here to not confuse with C language -->
the goal is to discover a polynomially bounded data-flow relation, 
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
These are denoted with coefficients $0, m, w, p$ and $\infty$ (in pymwp we use `o` for $0$ and `i` for $\infty$). 

One way to think about $\infty$ is derivation failure. Alternatively, obtaining an $\infty$-free result
implies existence of a polynomial growth bound, i.e., the program has the property of interest, or simply "success".


#### Example 1

For some programs the analysis is straightforward.   

<div class="container text-left"><div class="row"><div class="col col-md-4">
PROGRAM

```c
int foo(int x, int y){
  if (𝔹) {
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


This obtained matrix indicates that value growth of variables `x` and `y` is polynomially bounded in their inputs.

The truth value of the control expression does not matter. We substitute it with $\mathbb{B}$ for
"some `bool` expression".


#### Example 2

For more complicated programs, the inference procedure introduces _choices_. 
These are represented by complex polynomials.
Variables have different dependencies for different derivation choices.
These are captured by the _deltas_ appearing in the matrix.

Deltas are coded as pairs of $(i, j)$ with $i$ the value and $j$ the index in the domain.
Possible values of $i$ are $\{0,1,2\}$. Index $j$, of type $\mathbb{N}$, corresponds to a program point where a choice is made.

<div class="container text-left"><div class="row"><div class="col col-md-4">
PROGRAM

```c
int foo(int x, int y){
  while (𝔹) {
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


Only the rightmost choice produces a valid derivation because it does not contain $\infty$ coefficients.

### Analysis Result

A program is derivable when it can be assigned a matrix (of choice) without infinite coefficients.
We call this an _"mwp-bound"_.
The soundness theorem of the calculus guarantees that if some $\infty$-free choice exists, the 
program variables value growth is polynomially bounded in inputs.


Program fails the analysis if it is assigned a matrix that always contains infinite coefficients, no matter the choices.
Then it is not possible to establish polynomial growth bound. For these programs, pymwp reports $\infty$ result.


