int main(){
    int X1=1, X2=1, X3=1, X4=1, X5=1, X6=1;
    if (X3 == 0){
        X1 = X2+X1;
    }
    while(X4<100){
        X2 = X3+X5;
        X3 = X4+X5;
        X4 = X1+X5;
        if (X3 == 0){
            X6 = X2+X2;
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