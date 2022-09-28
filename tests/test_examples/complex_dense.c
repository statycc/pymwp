/* This example produces a dense matrix
 * with 43,046,721 different assignments. */

int foo(int X0, int X1, int X2, int X3, int X4){
    if (X0) {
    X2 = X4 + X3;
    X3 = X0 + X1;
    X4 = X1 + X2;
    X0 = X4 + X3;
    X1 = X0 + X4;
    X2 = X1 + X0;
    X3 = X2 + X1;
    X4 = X3 + X2;
    }
    else
    {
    X1 = X4 + X3;
    X3 = X0 + X2;
    X4 = X2 + X1;
    X0 = X4 + X3;
    X2 = X0 + X4;
    X1 = X2 + X0;
    X3 = X1 + X2;
    X4 = X3 + X1;
    }
}
