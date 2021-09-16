int foo(int x, int y, int x1, int x2, int x3) {
  x = 1;
  x1 = 1;
  x2 = 2;
  if (x > 0) x3 = 1;
  else x3 = x2;
  y = x3;
}