/* 
 * This example is inspired from Example 3.2
 * from the original paper "A Flow Calculus of 
 * mwp-Bounds for Complexity Analysis".
 * This example is re-used in Example 3.5.
 */

int foo(int X1, int X2, int X3){
    while (X3 > 0){
        X1 = X1 + X2;
    }
}
