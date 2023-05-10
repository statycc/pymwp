\pagebreak

## Infinite Program{#inf-prog}

A program that shows infinite coefficients for all choices.

### Analyzed Program: infinite_3.c

```c
int foo(int X1, int X2, int X3){
    if (X1 == 1){
        X1 = X2+X1;
        X2 = X3+X2;
    }
    while(X1<10){
        X1 = X2+X1;
    }
}
```

If you studied the previous example carefully, you will  observe that this example is _very similar_.
There is a subtle change: variable $\texttt{X0}$ has been removed and its usages changed to $\texttt{X1}$.
This example demonstrates how this seemingly small change impacts the analysis result.

### CLI Command

```console
pymwp infinite/infinite_3.c --fin --info --no_time
```

Output:

```text
INFO (result): foo is infinite
INFO (result): Possibly problematic flows:
INFO (result): X1 ➔ X1 ‖ X2 ➔ X1 ‖ X3 ➔ X1
INFO (result): Total time: 0.0 s (2 ms)
INFO (file_io): saved result in output/infinite_3.json
```

### Discussion

We can observe the result is $\infty$.
Thus, even a small change can change the analysis result entirely.

The output reveals the problem arises from how data flows
from source variables $\texttt{X1}$, $\texttt{X2}$, and $\texttt{X3}$, to target variable $\texttt{X1}$.
Observe that even though there is no direct assignment from $\texttt{X3}$ to $\texttt{X1}$, 
the analysis correctly identifies this dependency relation, that occurs through $\texttt{X2}$.

From the output, we have identified the point and source of failure.
Conversely, we know other variable pairs are not problematic.
By focusing on how to avoid "too strong" dependencies targeting variable $\texttt{X1}$, programmer may be
able to refactor and improve the program's complexity properties.


