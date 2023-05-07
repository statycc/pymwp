\pagebreak

## Challenge Example

Try to guess the outcome before determining the result with pymwp.

<h4>**Analyzed Program**</h4>

```c
void foo(int X0, int X1, int X2){
    if (X0 == 0) {
        X2 = X0 + X1;
    }
    else {
        X2 = X2 + X1;
    }
    X0 = X2 + X1;
    X1 = X0 + X2;
    while(X2 < 10) {
        X2 = X1 + X0;
    }
}
```

After seeing the various preceding examples of programs, with and without polynomial bounds, we present the following challenge.
By inspection, try to determine if this program is polynomially bounded in inputs.
Note that it is unknown whether the `while` loop will terminate, however this is not a problem for determining the result.


**Choose.** The program is...
 
<div class="form-check">
  <input class="form-check-input" type="radio" name="flexRadio" id="P required" required>
  <label class="form-check-label" for="flexRadioDefault1">Polynomially bounded in inputs</label>
</div>
<div class="form-check">
  <input class="form-check-input" type="radio" name="flexRadio" id="Infinite">
  <label class="form-check-label" for="flexRadioDefault2">Infinite</label>
</div>

<br/>

<a class="btn btn-primary" data-bs-toggle="collapse" href="#solution" role="button" aria-expanded="true"
aria-controls="solution">Reveal Solution</a>


<div class="collapse" id="solution"> 

<h4>**CLI Command**</h4>

```console
pymwp other/dense_loop.c --fin --no_time --info
```

Output:

```console
INFO (result): Bound: X0′ ≤ max(X0,X2)+X1 ∧ X1′ ≤ X0*X1*X2 ∧ X2′ ≤ max(X0,X2)+X1
INFO (result): Bound count: 81
INFO (result): Total time: 0.1 s (83 ms)
INFO (file_io): saved result in output/dense_loop.json
```


<h4>**Discussion**</h4>

Variables `X0` and `X1` dependencies are consistently polynomially bounded for all choices.
This is observable in the corresponding columns of the matrix, since they contain no $\infty$ coefficients.

The situation is different for variable `X2`, the rightmost column in the matrix. Multiple derivation choices fail.
From the matrix, and from the choice vector, we can also observe that the critical choice occurs at index 4.
It corresponds to the statement inside the `while` loop. Failure may occur independent of the which branch of the preceding conditional statement was selected.

There are, however, multiple sequences of choices that allow completing the derivation.
The choice vector indicated how to complete the derivation.
For example, choices $[0, 0, 0, 0, 2]$ and $[1, 2, 1, 1, 2]$ are valid.

Because a valid derivation exists, the solution is yes, the program is polynomially bounded in inputs.

</div> 

<br/>

