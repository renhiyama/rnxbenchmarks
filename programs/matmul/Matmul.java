public class Matmul {
    public static void main(String[] args) {
        int n = 256;
        int nn = n * n;
        long[] a = new long[nn], b = new long[nn], c = new long[nn];
        for (int i = 0; i < nn; i++) {
            int r = i / n;
            int col = i - r * n;
            a[i] = ((r * 7 + col * 13) % 16) - 8;
            b[i] = ((r * 13 - col * 7) % 16) - 8;
        }
        for (int r = 0; r < n; r++) {
            for (int k = 0; k < n; k++) {
                long aik = a[r * n + k];
                for (int j = 0; j < n; j++) {
                    c[r * n + j] += aik * b[k * n + j];
                }
            }
        }
        long sum = 0;
        for (int q = 0; q < nn; q++) sum += c[q];
        System.out.println("matmul checksum = " + sum);
    }
}
