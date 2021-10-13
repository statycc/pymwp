/*
 * This example produces a dense matrix
 * with infinite coefficients in it.
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
    while(X2){X2 = X1 + X0;}
}
