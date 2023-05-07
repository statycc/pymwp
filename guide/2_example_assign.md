\pagebreak

## Binary Assignment

This example shows that assigning a compounded expression to a variable results in correct analysis.

<h4>**Analyzed Program**</h4>

```c
void foo(int y1, int y2){
    y2 = y1 + y1;
} 
```

This program is simple, and it is straightforward to observe that its has a polynomial growth bound wrt. input variables.
The precise value of the bound is $\texttt{y1}^\prime \leq \texttt{y1}$ and  $\texttt{y2}^\prime \leq 2\; \cdot \texttt{y1}$.
From analysis perspective this example is interesting because binary operations introduce internal complexity in program analysis.

<h4>**CLI Command**</h4>


```console
pymwp basics/assign_expression.c --no_time --info
```

Output:

```console
INFO (result): Bound: y1′ ≤ y1 ∧ y2′ ≤ y1
INFO (result): Bound count: 3
INFO (result): Total time: 0.0 s (1 ms)
INFO (file_io): saved result in output/assign_expression.json
```

<h4>**Discussion**</h4>

The analysis correctly assigns a polynomial bound to the program.
The bound obtained by the analyzer is $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{y1}$,
which is correct, as the bound expression does not include constants.
Due to non-determinism, the analyzer finds 3 different derivations paths that yield a bound.
Revealing technical internals (not apparent in the output), these bounds are:  

- $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{max(0,0) + y1}$
- $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{max(0,0) + y1}$
- $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{max(0,y1) + 0}$

They all simplify to a bound $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{y1}$,
concluding the result matches the expected bound.

