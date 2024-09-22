void invalid_true(int x, int y, int z){
    if(true) x = *x + 1;
    else w = z + 1;
}

void partially_invalid_true(int x, int y, int z){
    if(true) {
        y = x + y;
        x = *x + 1;
    }
    else w = z + 1;
}

void invalid_else(int x, int y, int z){
    if(true) x = x + 1;
    else w = *z + 1;
}

void partially_invalid_else(int x, int y, int z){
    if(true) x = x + 1;
    else {
        z = z + 1;
        w = *z + 1;
    }
}

void invalid_branches(int x, int y, int z){
    if(true) x = *x + 1;
    else w = *z + 1;
}
