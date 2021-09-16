/*
 * This program tests that a simple program computing the 
 * exponentiation results in matrix with infinite coefficient in them.
 * Inspired from https://stackoverflow.com/a/213897
 */

int main(int x, int n, int p, int r){
    p = x;
    while (n > 0)
    {
        if (n % 2 == 1)
            r = p * r;
        p = p * p;
        n = n / 2;
    }
}
