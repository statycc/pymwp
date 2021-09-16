int foo(int x, int y, int x1, int x2, int x3) {
  if (x > 0) x3 = x1;
  else x3 = x2;
  y = x3;
}