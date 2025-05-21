int foo(int X0, int X1, int n){
    while(X1<n){
        X0 = X1*X0;
        X1 = X1+X0;
    }
}
