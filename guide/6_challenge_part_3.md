<div class="collapse" id="solution"> 

### CLI Command

```console
pymwp other/dense_loop.c --fin --no_time --info
```

Output:

```text
INFO (result): Bound: X0' ≤ max(X0,X2)+X1 ∧ X1' ≤ X0*X1*X2 ∧ X2' ≤ max(X0,X2)+X1
INFO (result): Bounds: 81
INFO (result): Total time: 0.0 s (29 ms)
INFO (file_io): saved result in output/dense_loop.json
```

### Discussion

Even with just 3 variables we can see---in the obtained bound expression and the number of bounds---that this is a complicated derivation problem.
The analyzer determines the program has a polynomial growth bound. 
Let us reason informally and intuitively why this obtained result is correct.

We can observe in the bound expression, that all three variables have complicated dependencies on one another; 
this corresponds to what is also observable in the input program.

Regarding variables $\texttt{X0}$ and $\texttt{X1}$,
observe there is no command, with either as a target variable, that would give rise to exponential value growth (need iteration).
Therefore, they must have polynomial growth bounds.

Variable $\texttt{X2}$ is more complicated.
The program has a `while` loop performing assignments to $\texttt{X2}$ (potentially problematic), and the `while` loop may or may not execute.

* Case 1: loop condition is initially false.
  Then, final value of $\texttt{X2}$ depends on the `if` statement, and in either branch, it will have polynomially bounded growth.

* Case 2: loop condition true -- at least one iteration will occur.
  The program iteratively assigns values to $\texttt{X2}$  inside the `while` loop.
  However, notice the command is loop invariant.
  No matter how many times the loop iterates, the final value of $\texttt{X2}$ is $\texttt{X1} + \texttt{X0}$.
  We already know those two variables have polynomial growth bounds.
  Therefore, $\texttt{X2}$ also grows polynomially w.r.t. its input values.

This reasoning concurs with the result determined by pymwp.

</div>
