//taken from SPEC CPU2006	hmmer/src/masks.c 	XNU

int nondet();

//O(n)
void xnu(int len, int beg, int end, int i, int k) {
//    beg = 0;
//    end = 0;
//    i = 0;
    while (i < len) {
        i = i + 1;
        if (nondet())
            end = i;
        if (nondet()) {
            k = beg;
            while (k < end)
                k = k + 1;
            end = i;
            beg = end;
        } else if (nondet()) {
            end = i;
            beg = end;
        }
    }
} 

