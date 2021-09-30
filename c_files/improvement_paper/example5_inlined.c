/*
 * This example is a part of a collection:
 *
 * (1) example5.c - calls function f from foo
 * (2) example_5_inlined.c - f is inlined within foo
 */

int foo(int X1, int X2, int X3, int X_1, int R) {
    X3 = X1 + X1;
    X2 = X3 + X1;
    X_1 = X2;
    R = X2;
    while(X_1) { R = R + R; }
    X1 = R;
}