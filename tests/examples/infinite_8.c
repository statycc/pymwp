int foo(int X0, int X1, int X2, int X3, int X4, int X5, int c0){
    if (X3 == 0){
        X1 = X2+X1;
    }
    while(X4<c0){
        X2 = X3+X5;
        X3 = X4+X5;
        X4 = X2+X5;
        if (X3 == 0){
            X0 = X2+X2;
        }
        else{
            X2 = X3+X4;
        }
    }
    if (X3 == 0){
        X1 = X2+X1;
    }
    else{
        X2 = X3+X1;
    }
    
}