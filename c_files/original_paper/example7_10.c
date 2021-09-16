/* 
 * This example is inspired from Example 7.10
 * from the original paper "A Flow Calculus of 
 * mwp-Bounds for Complexity Analysis".
  */

int foo(int X1, int X2, int X3){
    if (0) {X3 = X1 + X1;}
    else{X3 = X3 + X2;}
}
