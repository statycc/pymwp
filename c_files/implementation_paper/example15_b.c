/*
 * This example is a part of a collection:
 *
 * (1) example15_a.c - calls function f from foo
 * (2) example15_b.c - f is inlined within foo
 *
 * In this example function call is skipped by in-lining the function.
 */

int foo(int X1, int X2, int R) {
    X2 = X1 + X1;
    X_1 = X2;  /* rename input variables */
    R = X2;    /* rename returned variable */
    while(b) { R = X_1 + X_1; }  /* chunk */
    X1 = R;    /* return is removed */
}
