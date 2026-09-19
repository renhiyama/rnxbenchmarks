fn main() {
    let n: i32 = 400;
    let limit: i32 = 1000;
    let mut total: i64 = 0;
    let mut y = 0;
    while y < n {
        let ci = -1.5 + (y as f64) * (3.0 / (n as f64));
        let mut x = 0;
        while x < n {
            let cr = -2.0 + (x as f64) * (3.0 / (n as f64));
            let mut zr = 0.0;
            let mut zi = 0.0;
            let mut iter = 0;
            while zr * zr + zi * zi <= 4.0 && iter < limit {
                let tr = zr * zr - zi * zi + cr;
                zi = 2.0 * zr * zi + ci;
                zr = tr;
                iter += 1;
            }
            total += iter as i64;
            x += 1;
        }
        y += 1;
    }
    println!("mandel {n} total = {total}");
}
