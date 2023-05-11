\pagebreak

## Challenge Example

Try to guess the analysis outcome before determining the result with pymwp.

### Analyzed Program

```c
int foo(int X0, int X1, int X2){
    if (X0) {
      X2 = X0 + X1;
    }
    else{
      X2 = X2 + X1;
    }
    X0 = X2 + X1;
    X1 = X0 + X2;
    while(X2){
      X2 = X1 + X0;
    }
}
```

After seeing the various preceding examples -- with and without polynomial bounds -- we present the following challenge.
By inspection, try to determine if this program is polynomially bounded w.r.t. its input values.

It is unknown which `if` branch will be taken, and whether the `while` loop will terminate,
but this is not a problem for determining the result.
