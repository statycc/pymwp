int main(int x, int y, int z) {
    /* should be interpreted as loop x{y = y + z;} */
    for (int i = 0; i < x; i++){
        y = y + z;
    }
}
