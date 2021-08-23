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

int main(){
    int x0=1, x1=1, x2=1, x3=1, x4=1, x5=1, x6=1, x7=1, x8=1, x9=1, x10=1, x11=1, x12=1, x13=1, x14=1, x15=1, x16=1, x17=1;
    x0 = x1 + x2;
    x3 = x4 + x5;
    x6 = x7 + x8;
    x9 = x10 + x11;
    x12 = x13 + x14;
    x15 = x16 + x17;
}
 
