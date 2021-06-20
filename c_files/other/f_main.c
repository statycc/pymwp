/*
 * This example is a part of a collection of 3 examples:
 *
 * (1) f_alone.c - analysis of a function f in isolation
 * (2) f_inline.c - analysis when function f is inlined within main
 * (3) f_main.c  - analysis of main in isolation, without f
 */

int main() {
    int x;
    int y;
    x = 1;
    y = 1; // f(x);
}