/* 
 * This example is inspired from Example 3.1
 * from the original paper "A Flow Calculus of 
 * mwp-Bounds for Complexity Analysis"
 */

int foo(int X1, int X2){
    X1 = 1;
    while (X2 > 0){
        X1 = X1 + X1;
    }
}
