/* 
 * This example is inspired from Example 3
 * from the  paper "An extended and more 
 *  practical mwp flow analysis".
  */

int foo(int X1, int X2, int X3){
    if (0) {X1 = X1 + X2;}
    else{X1 = X1 - X3;}
}
