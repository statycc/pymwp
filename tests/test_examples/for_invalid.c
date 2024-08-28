int main(int x, int y) {
    /* iteration variable occurs in body => invalid */
    for (int i = 0; i < x; i++) {
        y = y + x;
    }
}