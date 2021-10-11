/* This example produces a dense matrix
 * with 43,046,721 different assignments.
 * It is recommended to analyze it with the 
 * --no-eval flag.
 * It takes ~40 s. to analyze this program
 * without computing the evaluations, 
 * but ~2 days if the evaluations are computed.
 */

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
