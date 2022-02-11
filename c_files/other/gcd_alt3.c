/*
 * Greatest common divisor
 * Iterative Euclid algorithm
 * Inspired by https://rosettacode.org/wiki/Greatest_common_divisor#C
 */

void gcd(int x1, int x2) {
//  if (x1 < 0) {x1 = -x1};
//  if (x2 < 0) {x2 = -x2};
  if (x2) while ((x1 = x1 % x2) && (x2 = x2 % x1)){continue;}
  // return value is x1 + x2.
}

