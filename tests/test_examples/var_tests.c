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

// purposely no params
void fun_do_wh(){
  switch (a)
  {
    case 1:
        break;
    default:
       do {
         y = z + z;
         z = z + 1;
         x = x - 1;
       } while(x > 0);
  }
}

// purposely no params
void fun_if(){
  if (a > 0) {
       do {
         y = z + z;
         z = z + 1;
         x = x - 1;
       } while(x > 0);
}}

int mycast(int count) {
   return (double) sum / count;
}