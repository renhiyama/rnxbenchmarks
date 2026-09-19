fn main() {
    let n: usize = 256;
    let nn = n * n;
    let mut a = vec![0i64; nn];
    let mut b = vec![0i64; nn];
    let mut c = vec![0i64; nn];
    let mut i = 0;
    while i < nn {
        let r = (i / n) as i64;
        let col = (i - r as usize * n) as i64;
        a[i] = ((r * 7 + col * 13) % 16) - 8;
        b[i] = ((r * 13 - col * 7) % 16) - 8;
        i += 1;
    }
    let mut r = 0;
    while r < n {
        let mut k = 0;
        while k < n {
            let aik = a[r * n + k];
            let mut j = 0;
            while j < n {
                c[r * n + j] += aik * b[k * n + j];
                j += 1;
            }
            k += 1;
        }
        r += 1;
    }
    let mut sum = 0i64;
    let mut q = 0;
    while q < nn {
        sum += c[q];
        q += 1;
    }
    println!("matmul checksum = {sum}");
}
