---
title: pymwp 
subtitle: User Guide
next: Getting Started
next_href: setup.html
---

pymwp ("paɪ m-w-p") is a tool for automatically performing 
<a href="https://en.wikipedia.org/wiki/Static_program_analysis" target="blank" rel="nofollow noreferrer">static analysis</a> 
on programs written in subset of C language.
It analyzes resource usage and determines if program variables' growth rates are no more than polynomially related to their inputs sizes.

The theoretical foundations are described in paper 
_<a href="https://doi.org/10.4230/LIPIcs.FSCD.2022.26" target="blank" rel="nofollow noreferrer">"mwp-Analysis Improvement and Implementation: Realizing Implicit Computational Complexity"</a>_.
The technique is generic and applicable to imperative languages. pymwp is a prototype implementation demonstrating this technique concretely on C programs.
The technique is originally inspired by
_<a href="https://doi.org/10.1145/1555746.1555752" target="blank" rel="nofollow noreferrer">"A Flow Calculus of mwp-Bounds for Complexity Analysis"</a>_.

This guide explains pymwp usage and behavior through several high-level examples.

The Program Property of Interest
---

For an imperative program, the goal is to discover a polynomially bounded data-flow relation, 
between its initial values $x_1,...,x_n$ and final value $x_1^\prime,...,x_n^\prime$.

For a program written in C language, this property can be presented as follows.   

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

The analysis is performed by applying inference rules to program's commands.
These inference rules assign matrices to commands. 
A matrix characterizing a program is obtained by compositional analysis of its commands.

A matrix contains coefficients representing _dependencies_ between program variables.
These coefficients are $0, m, w, p$ and $\infty$. 

<details>
<summary>Brief explanation of coefficients</summary>
<div class="card card-body">
The coefficients characterize how data flows between variables:

* $0$ --- no dependency
* $m$ --- maximal (of linear)
* $w$ --- weak polynomial
* $p$ --- polynomial
* $\infty$ --- infinite

Ordering:  $0 < m < w < p < \infty$.  
In pymwp $0$ is `0` and $\infty$ is `i`.
</div>
</details>

One way to think about $\infty$ is derivation failure. Alternatively, obtaining an $\infty$-free derivation
implies existence of a polynomial growth bound, i.e., the program has the property of interest, or that the program is derivable.

#### Example 1

For some programs the analysis is straightforward, although we omit the steps here. 
Since pymwp performs the computation automatically, it is best we focus here on how to interpret those results.

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

The generated matrix is labelled with input variable names. The top-row shows the data flow _target_ and the left column is the _source_ of data flow.
This matrix contains only non-infinity coefficients, which means $\texttt{x}$ and $\texttt{y}$ value growth is polynomially bounded in inputs.
We can confirm this by inspection: final values are $\texttt{x}' \leq \texttt{x}$ and $\texttt{y}' \leq \texttt{x}$.

#### Example 2

For more complicated programs, the inference procedure introduces derivation _choice_. 
This is represented by complex polynomials.
Then variables can have different dependencies for different derivation choices.

We capture this in a matrix with _polynomials_.
A polynomial is an ordered list of ordered _monomials_.
A monomial is a pair made of a coefficient and ordered list of _deltas_.
In other words, by making the derivation choices indicated by a list of deltas, we obtain the associated coefficient.

Deltas are pairs of $(i, j)$ where $i$ is the value and $j$ the index in the domain.
Value $i$ is one of $\{0,1,2\}$ and represents a derivation choice. 
Index $j$ corresponds to a program point where a choice occurs; effectively it is a counter.

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


In this program, target variable $\texttt{x}$ has different dependencies and some choices yield $\infty$ coefficients.
In fact, the matrix with polynomials compactly capture three derivation outcomes, as shown below.
But only one choice $(2,0)$ produces a valid derivation, because it does not contain any $\infty$ coefficients.
 
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




### Analysis Result

A program is derivable when it can be assigned a matrix, that for some choice does not contain infinite coefficients.
The soundness theorem of the calculus guarantees that if such choice exists, the program variables' value growth is polynomially bounded in inputs.


Program fails the analysis if it is assigned a matrix that always contains infinite coefficients, no matter the choices.
Then it is not possible to establish polynomial growth bound. For these programs pymwp reports "infinite" result.


