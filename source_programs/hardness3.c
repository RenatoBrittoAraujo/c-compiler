int main () {
    int x = 1, y;
    printf("%d\n", 1 + 2);
    x = 3;
    y = x + 4;
    printf("%d\n", x);
    print_thing();
    x = 1 + (3 + 1) + 2;
}

void print_thing() {
    printf("thing\n");
}