/*
 * This program tests that a simple program computing the 
 * exponentiation results in matrix with infinite coefficient in them.
 * Inspired from https://stackoverflow.com/a/213897
 * Lines 14--19 refactors n=n/2 to eliminate the division operator.
 */
int main(int x, int n, int p, int r, int d){
    p = x;
    while (n > 0)
    {
        if (n % 2 == 1)
            r = p * r;
        p = p * p;
        d = 0;
        while (n > 0){
            n = n - 2;
            d = d + 1;
        }
        n = d;
    }
}
