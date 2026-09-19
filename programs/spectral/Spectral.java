public class Spectral {
    static double evalA(int i, int j) {
        int ij = i + j;
        return 1.0 / (double) ((ij * (ij + 1) / 2) + i + 1);
    }

    static void timesAv(double[] v, double[] out, int n) {
        for (int i = 0; i < n; i++) {
            double s = 0.0;
            for (int j = 0; j < n; j++) s += evalA(i, j) * v[j];
            out[i] = s;
        }
    }

    static void timesA(double[] v, double[] out, int n) {
        for (int i = 0; i < n; i++) {
            double s = 0.0;
            for (int j = 0; j < n; j++) s += evalA(j, i) * v[j];
            out[i] = s;
        }
    }

    public static void main(String[] args) {
        int n = 300;
        double[] u = new double[n], v = new double[n], w = new double[n];
        for (int i = 0; i < n; i++) u[i] = 1.0;
        for (int it = 0; it < 10; it++) {
            timesAv(u, w, n);
            timesA(w, v, n);
            timesAv(v, w, n);
            timesA(w, u, n);
        }
        double vbv = 0.0, vv = 0.0;
        for (int k = 0; k < n; k++) { vbv += u[k] * v[k]; vv += v[k] * v[k]; }
        System.out.println("spectral checksum = " + (long) (vbv / vv * 1000000.0));
    }
}
