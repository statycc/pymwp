//taken from SPEC CPU2006	hmmer/src/weight.c SingleLinkCluster

int nondet();

//O(n^2)
void SingleLinkCluster(unsigned int n, int a, int b, int i) {
  a = n;
  b = 0;
  while(a > 0) {
    a = a - 1;
    b = b + 1;
    while(b > 0) {
      b = b - 1;
      i = n - 1;
      while(i > 0)
        if(a > 0 && nondet()) {
          a = a - 1;
          b = b + 1;
        }
        i = i - 1;
    }
  } 
}

