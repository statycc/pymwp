\pagebreak

## Binary Assignment

This example shows that assigning a compounded expression to a variable results in correct analysis.

### Analyzed Program: assign_expression.c

```c
int foo(int y1, int y2){
    y2 = y1 + y1;
} 
```


It is straightforward to observe that this program has a polynomial growth bound.
The precise value of that bound is $\texttt{y1}^\prime = \texttt{y1} \land \texttt{y2}^\prime \leq 2 * \texttt{y1}$.
Although the program is simple, it is interesting because binary operations introduce complexity in program analysis.

### CLI Command

The current working directory should be the location of unzipped examples from [Installation](#installation) Step 4.

```console
pymwp basics/assign_expression.c --fin --info --no_time
```

Output:

```text
INFO (result): Bound: y1' ≤ y1 ∧ y2' ≤ y1
INFO (result): Bounds: 3
INFO (result): Total time: 0.0 s (0 ms)
INFO (file_io): saved result in output/assign_expression.json
```

### Discussion

The analysis correctly assigns a polynomial bound to the program.
The bound obtained by the analyzer is $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{y1}$.
Comparing to the precise value determined earlier, this bound is correct, because we omit constants in the analysis results.

Due to non-determinism, the analyzer finds three different derivations that yield a bound.
From the `.json` file, that captures the analysis result in more technical detail,
it is possible to determine these three bounds are:  

- $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{max(0,0) + y1}$
- $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{max(0,0) + y1}$
- $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{max(0,y1) + 0}$

They all simplify to $\texttt{y1}^\prime \leq \texttt{y1} \land \texttt{y2}^\prime \leq \texttt{y1}$.
This concludes the obtained result matches the expected result.

