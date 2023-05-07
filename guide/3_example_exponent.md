\pagebreak

## Exponential Program

A program computing the exponentiation produces a matrix with infinite coefficient, no matter the choices.

<h4>**Analyzed Program**</h4>

```C
int main(int x, int n, int p, int r){
    p = x;
    while (n > 0)
    {
        if (n % 2 == 1)
            r = p * r;
        p = p * p;
        n = n / 2;
    }
}
```

This program's variables `p` and `r` grow exponentially.
It is impossible to find a polynomial growth bound, and the analysis is expected to report "infinity" result.
This example demonstrates how pymwp arrives to that conclusion.


<h4>**CLI Command**</h4>

```console
pymwp infinite/exponent_1.c --fin --no_time --info
```

Output:

```console
INFO (result): main is infinite
INFO (result): Possibly problematic flows:
INFO (result): x ➔ p, r ‖ n ➔ p, r ‖ p ➔ p, r ‖ r ➔ p, r
INFO (result): Total time: 0.0 s (8 ms)
INFO (file_io): saved result in output/exponent_1.json
```

<h4>**Discussion**</h4>

The matrix shows that the problematic variables  are `p` and `r`. 
In the program, inside the `while` loop, there are two critical multiplication operations that introduce choices (indices 1 and 2).
No matter what choice is made, it is not possible to obtain an $\infty$-free result.
This concludes the program does not pass the analysis.

