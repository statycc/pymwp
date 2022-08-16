/*
 * This example file illustrates the explosion of the number of cases.
 * For that particular program, 729 different derivations, and 
 * hence 729 matrices, are possible in the analys.
 * That type of program generates 3^{number of lines} matrices
 * with the original analysis.
 * 
 * Our optimization and treatment of matrix operations makes it
 * tractable to analyse rapidly such program, and to output a matrix
 * that reflects all the possible choices: it should be observed that two
 * different derivations can still result in the same matrix.
 */

int foo(
    int x0, int x1, int x2, int x3, int x4, int x5, int x6, int x7, int x8, int x9, 
    int x10, int x11, int x12, int x13, int x14, int x15, int x16, int x17){
    x0 = x1 + x2;
    x3 = x4 + x5;
    x6 = x7 + x8;
    x9 = x10 + x11;
    x12 = x13 + x14;
    x15 = x16 + x17;
}
