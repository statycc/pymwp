\pagebreak

## Exponential Program

A program computing the exponentiation returns an infinite coefficient, no matter the derivation strategy chosen.

### Analyzed Program: exponent_2.c

```C
int foo(int base, int exp, int i, int result){
    while (i < exp){
        result = result * base;
        i = i + 1;
    }
}
```

This program's variable $\texttt{result}$ grows exponentially.
It is impossible to find a polynomial growth bound, and the analysis is expected to report $\infty$-result.
This example demonstrates how pymwp arrives to that conclusion.


### CLI Command

```console
pymwp infinite/exponent_2.c --fin --info --no_time
```

Output:

```text
INFO (result): foo is infinite
INFO (result): Possibly problematic flows:
INFO (result): base ➔ result ‖ exp ➔ result ‖ i ➔ result ‖ result ➔ result
INFO (result): Total time: 0.0 s (2 ms)
INFO (file_io): saved result in output/exponent_2.json
```

### Discussion

The output shows that the analyzer correctly detects that no bound can be established, and we obtain $\infty$-result.
The output also gives a list of problematic flows.
This list indicates all variable pairs, that along some derivation paths, cause $\infty$ coefficients to occur.
The arrow direction means data flows from `source ➔ target`.
We can see the problem with this program is the data flowing to $\texttt{result}$ variable.
This clearly indicates the origin of the problem, and allows programmer to determine if the issue can be repaired, 
to improve program's complexity properties.


