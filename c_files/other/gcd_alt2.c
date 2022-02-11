/*
 * Greatest common divisor
 * - gcd by subtractions and swapping.
 * - temp is supposed to be given the value 0.
 */

void gcd(int x1, int x2, int temp, int result) {
    if(x2 > x1){
      temp = x1;
      x1 = x2;
      x2 = temp;
    }
    
    while(temp <= x2){
       if (x1 % temp == 0 && x2 % temp ==0) {
           result = temp;
       }
       temp = temp + 1;
    }
}
