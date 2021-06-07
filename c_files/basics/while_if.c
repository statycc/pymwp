/*
 * This program tests that a simple program containing 
 * while and if … else statements results in the correct analysis.
 */

int main(){
    int y1 = 1, y2 = 1, r = 1;
    while (0) {y2 = y1 + y1;}
    if (1) {r = y2;} else {r = y2 + y2;}
}
