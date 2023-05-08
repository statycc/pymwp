---
title: "pymwp: A Static Analyzer Determining Polynomial Growth Bounds"
subtitle: Paper Companion & User Guide
documentclass: scrartcl  
lang: en
fontsize: 10pt
numbersections: true
papersize: letter
geometry: margin=1in
secnumdepth: 2
author:
- Clément Aubert
- Thomas Rubiano
- Neea Rusch
- Thomas Seiller
keywords:
- Static Program Analysis
- Automatic Complexity Analysis
- Program Verification
---

\pagebreak

# Introduction

pymwp ("pai m-w-p") is a tool for automatically performing static analysis on programs written in subset of C language.
It analyzes resource usage and determines if program variables' growth rates are no more than polynomially related to their inputs sizes.

The theoretical foundations are described in paper "mwp-Analysis Improvement and Implementation: Realizing Implicit Computational Complexity".
The technique is generic and applicable to imperative languages. pymwp is a prototype implementation demonstrating this technique concretely on C programs.
The technique is originally inspired by "A Flow Calculus of mwp-Bounds for Complexity Analysis".

This guide explains pymwp usage and behavior through several high-level examples.

## Property of Interest

For an imperative program, the goal is to discover a polynomially bounded data-flow relation, 
between its initial values $x_1,...,x_n$ and final value $x_1^\prime,...,x_n^\prime$.

For a program written in C language, this property can be presented as follows.   

```c
void main(int X1, int X2, int X3){
   // initial values  ↑

   /*
    * various commands involving
    * variables X1, X2, X3
    */

   // X1', X2', X3' (final values)
}
```

Question: $\forall i$, is $\texttt{X}_i \rightsquigarrow \texttt{X}_i^\prime$ polynomially bounded in inputs? 

We answer this question using mwp-flow analysis implemented in static analyzer pymwp.

## Understanding mwp-flow Analysis Results

The mwp-flow analysis is performed by applying inference rules to program's commands.

Internally the analysis uses coefficients representing _dependencies_ between program variables.
These coefficients are $0, m, w, p$ and $\infty$.
The coefficients characterize how data flows between variables.

* $0$ --- no dependency
* $m$ --- maximal (of linear)
* $w$ --- weak polynomial
* $p$ --- polynomial
* $\infty$ --- infinite

Ordering:  $0 < m < w < p < \infty$.
The analysis name comes from these coefficients.

Successful analysis finds an mwp-bound for each input variable. An mwp-bound is an expression of form:

```
m-variables       p-variables
    ↓                    ↓ 
max(x, poly1(y)) + poly2(z)
             ↑  
       w-variables
```

where $x$, $y$, and $z$ are disjoint variable lists.
Each list may be empty and $poly_1$ and $poly_2$ may not be present.
The bound represents dependency of a variable on program's other input variables.

A bound expression can be formed if no pair of variables is characterized by $\infty$-flow.
One way to think about $\infty$ is derivation failure. Alternatively, obtaining an $\infty$-free derivation
implies existence of a polynomial growth bound, i.e., the program has the property of interest, or that the program is derivable.

This description is simplified and excludes many technical details. 
However, it is relevant to be aware that internally the analysis evaluates potentially exponential number of derivation paths.
This means it may assign exponential number of bounds to one program.

A program is derivable when a derivation exists that contains no infinite coefficients.
The soundness theorem of the mwp-calculus guarantees that if such choice exists, the program variables' value growth is polynomially bounded in inputs.

Program fails the analysis if every derivation contains infinite coefficients.
Then it is not possible to establish polynomial growth bound. 
For these programs, pymwp reports an $\infty$-result.
