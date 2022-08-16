int foo(int X0, int X1, int X2, int X3, int X4){
    while(X0<100){
        X0 = X2+X0;
        X2 = X3+X3;
        X3 = X1+X4;
        X1 = X0+X0;
    }
}

