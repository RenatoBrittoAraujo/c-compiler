#include <stdio.h>
#include <string.h>

int jose(int a) {
    return a == 1;
}

int jose(int* a) {
    return &a == 1;
}

int main() {
    int x = 1;
    printf("%d\n", jose(x));
    printf("%d\n", jose(&a));
}

// sem overload de função por assinatura