int main(int X1, int X2, int X3, int X4){
    if (X3 == 0){
        X1 = X2+X1;
    }
    else{
        X2 = X3+X2;
    }
    while(X2<100){
        X1 = X2+X4;
        X2 = X3+X4;
    }
    if (X3 == 0){
        X1 = X2+X1;
        X2 = X3+X2;
    }
}