int main(int X1, int X2, int X3, int X4){
    if (X3 == 0){
        X1 = X2+X1;
        X2 = X3+X2;
    }
    while(X4<10){
        X1 = X2+X4;
        X2 = X3+X3;
        X3 = X4+X4;
    }
}