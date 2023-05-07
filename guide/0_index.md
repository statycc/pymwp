---
title: "pymwp: A Static Analyzer Determining Polynomial Growth Bounds"
subtitle: User Guide
lang: en
fontsize: 10pt
documentclass: scrartcl  
numbersections: true     
papersize: letter        
geometry: margin=1in     
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

We answer this question using mwp-flow analysis, implemented in static analyzer pymwp.

## Understanding mwp-flow Analysis Results

The mwp-flow analysis is performed by applying inference rules to program's commands.

Internally the analysis uses coefficients representing _dependencies_ between program variables.
These coefficients are $0, m, w, p$ and $\infty$. The analysis name also comes from these coefficients.

The coefficients characterize how data flows between variables.

* $0$ --- no dependency
* $m$ --- maximal (of linear)
* $w$ --- weak polynomial
* $p$ --- polynomial
* $\infty$ --- infinite

Ordering:  $0 < m < w < p < \infty$. 

Successful analysis finds an mwp-bound for each variable. An mwp-bound is an expression of form:

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

A bound expression assumes no pair of variables is characterized by $\infty$-flow.
One way to think about $\infty$ is derivation failure. Alternatively, obtaining an $\infty$-free derivation
implies existence of a polynomial growth bound, i.e., the program has the property of interest, or that the program is derivable.

This description is simplified and excludes technical details. 
Internally the analysis evaluates potentially exponential number of
derivation paths, and may assign multiple bounds (exponential in number of assignments) to one program.

A program is derivable when a derivation exists that contains no infinite coefficients.
The soundness theorem of the calculus guarantees that if such choice exists, the program variables' value growth is polynomially bounded in inputs.

Program fails the analysis if every derivation contains infinite coefficients.
Then it is not possible to establish polynomial growth bound. 
For these programs, pymwp reports $\infty$-result.
