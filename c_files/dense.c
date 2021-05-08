int main(){
    int X0=1, X1=1, X2=1, X3=1, X4=1;
    if (X2==1) {
    X2 = X4 + X3;
    X3 = X0 + X1;
    X4 = X1 + X2;
    X0 = X4 + X3;
    X1 = X0 + X4;
    X2 = X1 + X0;
    X3 = X2 + X1;
    X4 = X3 + X2;
    }
    else
    {
    X1 = X4 + X3;
    X3 = X0 + X2;
    X4 = X2 + X1;
    X0 = X4 + X3;
    X2 = X0 + X4;
    X1 = X2 + X0;
    X3 = X1 + X2;
    X4 = X3 + X1;
    }
}
