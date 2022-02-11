/*
 * Greatest common divisor
 * Iterative Euclid algorithm
 * Inspired by https://rosettacode.org/wiki/Greatest_common_divisor#C
 * This algo is "cheating" in the sense that a lot happens in the condition for
 * while, which is not evaluated.
 */

void gcd(int x1, int x2) {
    // The following two statements are problematic:
    //  if (x1 < 0) {x1 = -x1};
    //  if (x2 < 0) {x2 = -x2};
    // We should implement unary minus and interpret it simply as x1 = x1, since
    // dependent-wise it is the same.
  if (x2) while ((x1 = x1 % x2) && (x2 = x2 % x1)){continue;}
  // return value is x1 + x2.
}

