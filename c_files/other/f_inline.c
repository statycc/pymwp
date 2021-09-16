/*
 * This example is a part of a collection of 3 examples:
 *
 * (1) f_alone.c - analysis of a function f in isolation
 * (2) f_inline.c - analysis when function f is inlined within main
 * (3) f_main.c  - analysis of main in isolation, without f
 */

int foo(int y, int x, int x1, int x2, int x3) {
    if(x > 0) x3 = x1;
    else x3 = x2;
    y = x3;
}