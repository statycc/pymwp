int main(){
    int X1=1, X2=1, X3=1, X4=1,X5=1;
    while(X1<100){
        X1 = X2+X2;
        X2 = X3+X3;
        X3 = X4+X4;
        X4 = X5+X5;
    }
    if (X1 == 1){
        X1 = X2+X1;
        X2 = X3+X2;
    }
    while(X1<100){
        X1 = X2+X1;
    }
}