/*
 * Greatest common divisor
 * - gcd by subtractions and swapping.
 */
void gcd(int x1, int x2, int temp) {
  while (x1 > 0 && x2 > 0) {
    if (x1 > x2){
      x1 = x1 - x2;
    }
    else{
      temp = x1;
      x1 = x2;
      x2 = temp;
    }        
  }
}
