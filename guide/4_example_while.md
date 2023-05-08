\pagebreak

## While Analysis

A program that shows infinite coefficients for some derivations.

### Analyzed Program: notinfinite_3.c

```c
int foo(int X0, int X1, int X2, int X3){
    if (X1 == 1){
        X1 = X2+X1;
        X2 = X3+X2;
    }
    while(X0<10){
        X0 = X1+X2;
    }
}
```

This program contains decision logic, iteration, and multiple variables.
Determining if a polynomial growth bound exists is not immediate by inspection.
It is therefore an interesting candidate for analysis with pymwp!

### CLI Command

```console
pymwp not_infinite/notinfinite_3.c --fin --info --no_time
```

Output: 

```text
INFO (result): Bound: X0' ≤ max(X0,X1)+X2*X3 ∧ X1' ≤ X1+X2 ∧ X2' ≤ X2+X3 ∧ X3' ≤ X3
INFO (result): Bounds: 9
INFO (result): Total time: 0.0 s (3 ms)
INFO (file_io): saved result in output/notinfinite_3.json
```

### Discussion

Compared to previous examples, the analysis is now getting more complicated.
We can observe this in the number of discovered bounds and the form of the bound expression.
The number of times the loop iterates, or which branch of the `if` statement is taken, is not a barrier to determining the result.

From the bound expression, we can determine the following.

* $\texttt{X0}$ has the most complicated dependency relation.
  Its mwp-bound combines the impact of the `if` statement, the `while` loop, and the chance that
  the loop may not execute.

* $\texttt{X1}$ and $\texttt{X2}$ have fairly simple growth dependencies; originating from the `if` statement.

* $\texttt{X3}$ is the most simple case -- it never changes. Therefore, it only depends on itself.

Overall, the analysis concludes the program has a polynomial growth bound.
