/*
 * This example is a part of a collection:
 *
 * (1) example14.c - calls function f from foo
 * (2) example16.c - f is inlined within foo
 *
 * In this example function call is skipped by in-lining the function.
 */

int foo(int X1, int X2, int X_1, int R) {
    X2 = X1 + X1;
    X_1 = X2;  /* rename input variables */
    while(b) { R = X_1 + X_1; }  /* chunk */
    X1 = R;    /* return is removed */
}
