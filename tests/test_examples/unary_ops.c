int foo(int x, int y){
    x++;
    ++x;
    y--;
    --x;
    sizeof((int)x); // skip
    // sizeof(*x); // invalid
    x = ++y;
    y = y++;
    x = !x;
    x = -x;
    y = sizeof(!x);  // recursive unary
}