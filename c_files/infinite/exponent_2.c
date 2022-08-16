/*
 * This program tests that a simple program computing the 
 * exponentiation results in matrix with infinite coefficient in them.
 * 
 * Inspired from https://stackoverflow.com/a/213322
 */

int foo(int base, int exp, int i, int result){
    while (i < exp){
        result = result * base;
        i = i + 1;
    }
}
