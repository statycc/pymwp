int foo(int x, int y){
    x++;
    ++x;
    x--;
    --x;
    sizeof(x); // skip
    sizeof(*x); // invalid
    x = ++x;
    y = x++;
    x = --y;
    x = !x;
    x = +x;
    y = sizeof(!x);  // recursive unary
}