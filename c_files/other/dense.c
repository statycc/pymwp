/*
 * This example produces a 3 x 3
 * dense matrix.
 */

int foo(int X0, int X1, int X2){
    if (X0) {
    X2 = X0 + X1;
    }
    else
    {
    X2 = X2 + X1;
    }
    X0 = X2 + X1;
    X1 = X0 + X2;
}
