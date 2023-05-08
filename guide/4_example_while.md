\pagebreak

## While Analysis

A program that shows infinite coefficients for some choices.

### Analyzed Program

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

This program contains decision logic, a while loop, and multiple variables.
Determining if a polynomial growth bound exists is not immediate by inspection.
It is therefore an interesting candidate for analysis with pymwp!

### CLI Command

```console
pymwp not_infinite/notinfinite_3.c --fin --info --no_time
```

Output: 

```console
INFO (result): Bound: X0' ≤ max(X0,X1)+X2*X3 ∧ X1' ≤ X1+X2 
∧ X2' ≤ X2+X3 ∧ X3' ≤ X3
INFO (result): Bound count: 9
INFO (result): Total time: 0.0 s (9 ms)
INFO (file_io): saved result in output/notinfinite_3.json
```


### Discussion

Compared to previous examples, the matrix is now getting more complicated.
The choice vector tells us that every derivation choice is allowed at indices 0 and 1 . These correspond to the operations inside the `if` statement.
But inside the `while` loop, only choice 2 is allowed to obtain a valid derivation result.
Because there exists a choice for which the program is derivable, this program's variable values growth is bounded by polynomials in inputs.

