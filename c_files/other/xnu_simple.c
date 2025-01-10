// Fig. 1 in Sinn et al. <https://doi.org/10.1007/s10817-016-9402-4>
int nondet();

void xnuSimple(int n, int p) {
    int x = n;
    int r = 0;
    while(x > 0) {
        x = x - 1;
        r = r + 1;
        if(nondet()) {
            p = r;
            while(p > 0)
              p--;
            r = 0;
        }
    }
}
