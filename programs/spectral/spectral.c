#include <stdio.h>
#include <stdlib.h>

static double eval_a(int i, int j) {
    int ij = i + j;
    return 1.0 / (double)((ij * (ij + 1) / 2) + i + 1);
}

static void times_av(double *v, double *out, int n) {
    for (int i = 0; i < n; i++) {
        double s = 0.0;
        for (int j = 0; j < n; j++) s += eval_a(i, j) * v[j];
        out[i] = s;
    }
}

static void times_a(double *v, double *out, int n) {
    for (int i = 0; i < n; i++) {
        double s = 0.0;
        for (int j = 0; j < n; j++) s += eval_a(j, i) * v[j];
        out[i] = s;
    }
}

int main(void) {
    const int n = 300;
    double *u = malloc((size_t)n * sizeof(double));
    double *v = malloc((size_t)n * sizeof(double));
    double *w = malloc((size_t)n * sizeof(double));
    for (int i = 0; i < n; i++) { u[i] = 1.0; v[i] = 0.0; w[i] = 0.0; }
    for (int it = 0; it < 10; it++) {
        times_av(u, w, n);
        times_a(w, v, n);
        times_av(v, w, n);
        times_a(w, u, n);
    }
    double vbv = 0.0, vv = 0.0;
    for (int k = 0; k < n; k++) { vbv += u[k] * v[k]; vv += v[k] * v[k]; }
    printf("spectral checksum = %ld\n", (long)(vbv / vv * 1000000.0));
    free(u); free(v); free(w);
    return 0;
}
