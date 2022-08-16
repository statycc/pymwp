int main(int X1, int X2, int X3, int X4, int X5){
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
    while(X1<10){
        X1 = X2+X2;
    }
}