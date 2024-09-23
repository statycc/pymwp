/* 
 * This example is inspired from Example 3.4
 * from the original paper "A Flow Calculus of 
 * mwp-Bounds for Complexity Analysis"
 */
int foo(int X1, int X2, int X3, int X4, int X5){

    for(int i = 0; i < X1; i++) {
        /*
         * The original example reads
         * X3 = X2 * X2 + X5;
         * but we are decomposing that statement in two:
         */
        X3 = X2 * X2;
        X3 = X3 + X5;
        X4 = X4 + X5;
    }
}
