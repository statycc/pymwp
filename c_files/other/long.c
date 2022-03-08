/*
 * Longer C program
 */
int foo(int X0, int X1, int X2, int X3, int X4){

    X0 = X2 + X1;
    X1 = X0 + X2;

    if (X0) {
        X2 = X0 + X1;
    }
    else{
        X2 = X2 + X1;
    }

    while(X2){
        X2 = X1 + X0;
    }

    if(X1){
        if(X2){
            X3 = X2;
        }
        else{
            X0 = X1 + X4;
        }
        if(X1){
            if(X3){
                X1 = X3;
            }
            else{
                X1 = X4;
            }
        }
    }

    X4 = X3 + X2;
    X4 = X4 - X1;
    X4 = X4 * X0;

    while(X0){
        X2 = X0 + X1;
        break;
    }
}
