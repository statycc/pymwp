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
The technique is generic and applicable to imperative languages. 
pymwp is an implementation demonstrating this technique concretely on C programs.
The technique is originally inspired by "A Flow Calculus of mwp-Bounds for Complexity Analysis".

This guide explains pymwp usage and behavior through several examples.

## Property of Interest

For an imperative program, the goal is to discover a polynomially bounded data-flow relation, 
between its initial values $\texttt{X}_1,...,\texttt{X}_n$ and final value $\texttt{X}_1^\prime,...,\texttt{X}_n^\prime$.

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

We answer this question with mwp-flow analysis, implemented in pymwp static analyzer.

## What mwp-flow Analysis Computes

The mwp-flow analysis works to establish a polynomial growth bound for input variables by applying inference rules to program's commands.

Internally, the analysis tracks _coefficients_ representing _dependencies_ between program's variables.
These coefficients (or "flows") are $0, m, w, p$ and $\infty$.
They characterize how data flows between variables.

* $0$ --- no dependency
* $m$ --- maximal (of linear)
* $w$ --- weak polynomial
* $p$ --- polynomial
* $\infty$ --- infinite

Ordering:  $0 < m < w < p < \infty$.
The analysis name also comes from these coefficients.

After analysis, two outcomes are possible.
(A) The program has a polynomial growth, or (B) the analysis determines it is impossible to establish such a bound.
Due to non-determinism, may derivation paths need to be explored to determine this result.

The analysis succeeds if -- for some derivation -- no pair of variables is characterized by $\infty$-flow.
That is, obtaining an $\infty$-free derivation implies existence of a polynomial growth bound; 
i.e., the program has the property of interest, or we can say that the program is _derivable_.
The soundness theorem of the mwp-calculus guarantees that if such derivation exists, the program variables' value growth is polynomially bounded in inputs.

Program fails the analysis if every derivation contains infinite coefficients.
Then it is not possible to establish polynomial growth bound.
For these programs, pymwp reports an $\infty$-result.

## Interpreting mwp-Bounds

If the analysis is successful, i.e. polynomial growth bound exists, it is represented using an _mwp-bound_.

An mwp-bound is a number theoretic expression of form: $\text{max}(\vec x, poly_1(\vec y)) + poly_2(\vec z)$.

Disjoint variable lists $\vec x$, $\vec y$ and $\vec z$ capture dependencies of an input variable.
Dependencies characterized by $m$-flow are in $\vec x$, $w$-flow in $\vec y$, and $p$-flow in $\vec z$.
The polynomials $poly_1$ and $poly_2$ are built up from constants and variables, and operators $+$ and $\times$.
Each variable list may be empty and $poly_1$ and $poly_2$ may not be present.

For multiple input variables, the result is a conjunction of mwp-bounds, one for each input variable.

**Example.** Using the mwp-bound expression, the analysis can produce various results.
This example gives intuition of how to interpret some possible results.

Obtained bound: $\texttt{X}' \leq \texttt{X}$   

- Assume program has one input variable named $\texttt{X}$.
- The bound expression means the final value $\texttt{X}'$ depends only on its own input $\texttt{X}$.

Obtained bound: $\texttt{X}' \leq \texttt{X} \land \texttt{Y}' \leq \text{max}(\texttt{X}, 0) + \texttt{Y}$   

- Assume program has two inputs, $\texttt{X}$ and $\texttt{Y}$.
- Final value $\texttt{X}'$ depends on its own input $\texttt{X}$.
- Final value $\texttt{Y}'$ depends on inputs $\texttt{X}$ and $\texttt{Y}$.
- The expression can be simplified to: $\texttt{X}' \leq \texttt{X} \land \texttt{Y}' \leq \texttt{X} + \texttt{Y}$.


