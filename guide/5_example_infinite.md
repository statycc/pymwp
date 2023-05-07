\pagebreak

## Infinite Program

A program that shows infinite coefficients for all choices.

<h4>**Analyzed Program**</h4>

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


Compared to the previous example, this program looks very similar.
But we remove variable `X0` and change its usages: the loop condition and assignment inside the `while` loop.
This example demonstrates how this seemingly small change impacts the analysis result. 
The page title obviously reveals the outcome, but let us see why.

<h4>**CLI Command**</h4>

```console
pymwp infinite/infinite_3.c --fin --info --no_time
```

Output:

```console
INFO (result): foo is infinite
INFO (result): Possibly problematic flows:
INFO (result): X1 ➔ X1 ‖ X2 ➔ X1 ‖ X3 ➔ X1
INFO (result): Total time: 0.0 s (6 ms)
INFO (file_io): saved result in output/infinite_3.json
```

<h4>**Discussion**</h4>

The two rightmost matrix columns do not contain $\infty$ coefficients. 
This means data flow to variables `X2` and `X3` have polynomially bounded growth.
The problematic variable is `X1`.
Observe that it is impossible to make a choice, at index 2, that would produce a matrix without infinite coefficients.
This corresponds to the assignment statement inside the `while` loop. 
Thus, we have identified the point and source of failure. 
The conclusion of this analysis is $\infty$ result. 

