/*
 * This example is a part of a collection:
 *
 * (1) example5.c - calls function f from foo
 * (2) example_5_inlined.c - f is inlined within foo
 */

int f(int X1, int X2){
    while(X1) { X2 = X2 + X2; }
    return X2;
}

int foo(int X1, int X2, int X3) {
    X3 = X1 + X1;
    X2 = X3 + X1;
    X1 = f(X2, X2);
}