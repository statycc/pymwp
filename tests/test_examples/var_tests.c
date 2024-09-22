void loop(int X1){
  for (i = max (*minkey, findx1[icurlet]); i <= findx2[icurlet]; i++){
    X1++;
  }
}

void fcall(int X1, int X2){
    my_fun(X1, X2, X3, z);
}

void pointer_loop(int *level, int z){
   for (j = 0; j < *level; j++)
     z++;
}

void ok_loop(int x, int y, int z){
   for (int i = 0; i < x; i++)
     y = z + z;
}
void invalid_body(int x, int y){
   for (int i = 0; i < x; i++)
     foo(y);
}
void partially_invalid_body(int x, int y){
   for (int i = 0; i < x; i++){
     foo(y);
     y = y + 1;
   }
}

void fun_do_wh(){
  switch (a)
  {
    case 1:
        break;
    default:
       do {  y = z + z; z = z + 1; x = x - 1; } while(x > 0);
  }
}

void fun_if(){ // purposely no params
  if (a > 0) { do {  y = z + z; z = z + 1; x = x - 1; } while(x > 0); }
}

int cast(int count) {
   return (double) sum * count;
}

void triple(int X1, int X2, int X3){
    X1 = X1 + X2 + X3;
}

void arr(int x, int some_var, int* my_arrC){
    my_arrC[x][x] = 1;
    some_var = x;
}

void ignore_tf(int X1, int X2){
    while(true){
       X1 = X1 + X2;
    }
}
