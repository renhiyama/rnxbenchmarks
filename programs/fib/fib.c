#include <stdio.h>

static long fib(long n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    printf("fib(35) = %ld\n", fib(35));
    return 0;
}
