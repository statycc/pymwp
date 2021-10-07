int foo(int X0, int X1, int X2){
    if (X2) {
    X2 = X2 + X1;
    X1 = X0 + X1;
    X0 = X1 + X2;
    }
    else
    {
    X2 = X0 + X1;
    }
}
