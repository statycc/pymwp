/*
 * This example is a part of a collection of 3 examples:
 *
 * (1) f_alone.c - analysis of a function bar in isolation
 * (2) f_inline.c - analysis where function bar is inlined within foo
 * (3) f_main.c  - analysis of foo in isolation, without bar
 */

int bar(int x, int x1, int x2, int x3){
    if(x > 0) x3 = x1;
    else x3 = x2;
    return x3;
}