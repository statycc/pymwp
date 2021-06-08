int main(){
    int X0=1, X1=1, X2=1, X3=1;
    if (X1 == 1){
        X1 = X2+X1;
        X2 = X3+X2;
    }
    while(X0<10){
        X0 = X1+X2;
    }
}