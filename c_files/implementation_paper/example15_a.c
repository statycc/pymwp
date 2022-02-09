/*
 * This example is a part of a collection:
 *
 * (1) example15_a.c - calls function f from foo
 * (2) example15_b.c - f is inlined within foo
 *
 * In this example two functions are analyzed separately.
 */

int f(int X1, int X2){
    while(X1) { X2 = X1 + X1; }
    return X2;
}

int foo(int X1, int X2) {
    X2 = X1 + X1;
    X1 = f(X2, X2);  /* function call */
    /*
     * Note: this function call is currently not yet analyzed in the
     * implementation of pymwp, and as such the two examples
     * example15_a.c/example15_b.c do not produce comparable matrices.
     * Once analysis of function calls is fully implemented, the matrices
     * will be comparable.
     */
}
