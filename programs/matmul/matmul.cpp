#include <cstdio>
#include <vector>

int main() {
    const int n = 256;
    const int nn = n * n;
    std::vector<int> a(nn), b(nn), c(nn, 0);
    for (int i = 0; i < nn; i++) {
        int r = i / n;
        int col = i - r * n;
        a[i] = ((r * 7 + col * 13) % 16) - 8;
        b[i] = ((r * 13 - col * 7) % 16) - 8;
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
    return 0;
}
