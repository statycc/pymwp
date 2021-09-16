#include <stdio.h>

int foo(int y) {
    y = 1;
    for (int x = 0; x < y; x++){y++; printf("%d", x);}
} 
