/*
 * Greatest common divisor
 * - gcd by subtractions.
 */
void gcd(int x, int y) {
  while (x > 0 && y > 0) {
    if (x > y)
      x = x - y;
    else
      y = y - x;
  }
}
