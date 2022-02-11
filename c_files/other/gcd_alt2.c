/*
 * Greatest common divisor
 * - gcd by subtractions and swapping.
 * - counter is supposed to be given the value 0.
 * - increment is supposed to be given the value 1.
 */

void gcd(int x1, int x2, int temp, int counter, int increment, int result) {
    if(x2 > x1){
      temp = x1;
      x1 = x2;
      x2 = temp;
    }
    
    while(counter <= x2){
       if (x1 % counter == 0 && x2 % counter ==0) {
           result = counter;
       }
       counter = counter + increment;
    }
}
