/* x not allowed to occurs in loop body ==> add x_ and substitute */
int main(int x, int y, int x_) {
    x_ = x;
    for (int i = 0; i < x; i++) {
        y = y + x_;
    }
}