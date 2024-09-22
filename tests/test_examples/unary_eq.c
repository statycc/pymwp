int foo(int x, int y){
    x = x + 1;
    x = x + 1;
    y = y - 1;
    x = x - 1;
    sizeof((int)x); // skip
    // sizeof(*x); // invalid
    y = 1 + y; x = y;
    y = y; y = y + 1;
    x = 1;
    x = x * 1;
    y = 0;
}