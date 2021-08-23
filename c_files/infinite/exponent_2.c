/*
 * This program tests that a simple program computing the 
 * exponentiation results in matrix with infinite coefficient in them.
 * 
 * Inspired from https://stackoverflow.com/a/213322
 */

int main(){
    int base;
    int exp;
    int i = 0;
    int result = 1;
    
    while (i < exp){
        result = result * base;
        i = i + 1;
    }
}
