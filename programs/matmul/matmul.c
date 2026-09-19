#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const int n = 256;
    const int nn = n * n;
    int *a = malloc((size_t)nn * sizeof(int));
    int *b = malloc((size_t)nn * sizeof(int));
    int *c = malloc((size_t)nn * sizeof(int));
    for (int i = 0; i < nn; i++) {
        int r = i / n;
        int col = i - r * n;
        a[i] = ((r * 7 + col * 13) % 16) - 8;
        b[i] = ((r * 13 - col * 7) % 16) - 8;
        c[i] = 0;
    }
    for (int r = 0; r < n; r++) {
        for (int k = 0; k < n; k++) {
            int aik = a[r * n + k];
            for (int j = 0; j < n; j++) {
                c[r * n + j] += aik * b[k * n + j];
            }
        }
    }
    long sum = 0;
    for (int q = 0; q < nn; q++) sum += c[q];
    printf("matmul checksum = %ld\n", sum);
    free(a); free(b); free(c);
    return 0;
}
