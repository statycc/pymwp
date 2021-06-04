int main() {
    int y = 1;
// Should be interpreted as
// loop x{y = y + x;}
    for (int x = 0; x < 10; x++){y = y + x;}
} 
