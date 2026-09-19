fn eval_a(i: i64, j: i64) -> f64 {
    let ij = i + j;
    1.0 / (((ij * (ij + 1) / 2) + i + 1) as f64)
}

fn times_av(v: &[f64], out: &mut [f64], n: usize) {
    let mut i = 0;
    while i < n {
        let mut s = 0.0;
        let mut j = 0;
        while j < n {
            s += eval_a(i as i64, j as i64) * v[j];
            j += 1;
        }
        out[i] = s;
        i += 1;
    }
}

fn times_a(v: &[f64], out: &mut [f64], n: usize) {
    let mut i = 0;
    while i < n {
        let mut s = 0.0;
        let mut j = 0;
        while j < n {
            s += eval_a(j as i64, i as i64) * v[j];
            j += 1;
        }
        out[i] = s;
        i += 1;
    }
}

fn main() {
    let n: usize = 300;
    let mut u = vec![1.0; n];
    let mut v = vec![0.0; n];
    let mut w = vec![0.0; n];
    let mut it = 0;
    while it < 10 {
        times_av(&u, &mut w, n);
        times_a(&w, &mut v, n);
        times_av(&v, &mut w, n);
        times_a(&w, &mut u, n);
        it += 1;
    }
    let mut vbv = 0.0;
    let mut vv = 0.0;
    let mut k = 0;
    while k < n {
        vbv += u[k] * v[k];
        vv += v[k] * v[k];
        k += 1;
    }
    println!("spectral checksum = {}", (vbv / vv * 1000000.0) as i64);
}
