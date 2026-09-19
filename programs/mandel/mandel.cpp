#include <cstdio>

int main() {
    const int n = 400;
    const int limit = 1000;
    long total = 0;
    for (int y = 0; y < n; y++) {
        double ci = -1.5 + (double)y * (3.0 / (double)n);
        for (int x = 0; x < n; x++) {
            double cr = -2.0 + (double)x * (3.0 / (double)n);
            double zr = 0.0, zi = 0.0;
            int iter = 0;
            while (zr * zr + zi * zi <= 4.0 && iter < limit) {
                double tr = zr * zr - zi * zi + cr;
                zi = 2.0 * zr * zi + ci;
                zr = tr;
                iter++;
            }
            total += iter;
        }
    }
    printf("mandel %d total = %ld\n", n, total);
    return 0;
}
