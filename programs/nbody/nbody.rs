fn push5(a: &mut [f64; 5], v: [f64; 5]) {
    a.copy_from_slice(&v);
}

fn offset_momentum(
    _x: &[f64; 5], _y: &[f64; 5], _z: &[f64; 5],
    vx: &mut [f64; 5], vy: &mut [f64; 5], vz: &mut [f64; 5], m: &[f64; 5],
) {
    let mut px = 0.0;
    let mut py = 0.0;
    let mut pz = 0.0;
    let mut i = 0;
    while i < 5 {
        px += vx[i] * m[i];
        py += vy[i] * m[i];
        pz += vz[i] * m[i];
        i += 1;
    }
    vx[0] = 0.0 - px / 1.0;
    vy[0] = 0.0 - py / 1.0;
    vz[0] = 0.0 - pz / 1.0;
}

fn advance(
    x: &mut [f64; 5], y: &mut [f64; 5], z: &mut [f64; 5],
    vx: &mut [f64; 5], vy: &mut [f64; 5], vz: &mut [f64; 5], m: &[f64; 5], dt: f64,
) {
    let mut i = 0;
    while i < 5 {
        let mut j = i + 1;
        while j < 5 {
            let dx = x[i] - x[j];
            let dy = y[i] - y[j];
            let dz = z[i] - z[j];
            let dsq = dx * dx + dy * dy + dz * dz;
            let dist = dsq.sqrt();
            let mag = dt / (dsq * dist);
            vx[i] -= dx * m[j] * mag;
            vy[i] -= dy * m[j] * mag;
            vz[i] -= dz * m[j] * mag;
            vx[j] += dx * m[i] * mag;
            vy[j] += dy * m[i] * mag;
            vz[j] += dz * m[i] * mag;
            j += 1;
        }
        i += 1;
    }
    let mut k = 0;
    while k < 5 {
        x[k] += dt * vx[k];
        y[k] += dt * vy[k];
        z[k] += dt * vz[k];
        k += 1;
    }
}

fn energy(
    x: &[f64; 5], y: &[f64; 5], z: &[f64; 5],
    vx: &[f64; 5], vy: &[f64; 5], vz: &[f64; 5], m: &[f64; 5],
) -> f64 {
    let mut e = 0.0;
    let mut i = 0;
    while i < 5 {
        e += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i]);
        let mut j = i + 1;
        while j < 5 {
            let dx = x[i] - x[j];
            let dy = y[i] - y[j];
            let dz = z[i] - z[j];
            let dist = (dx * dx + dy * dy + dz * dz).sqrt();
            e -= (m[i] * m[j]) / dist;
            j += 1;
        }
        i += 1;
    }
    e
}

fn main() {
    let mut x = [0.0; 5];
    let mut y = [0.0; 5];
    let mut z = [0.0; 5];
    let mut vx = [0.0; 5];
    let mut vy = [0.0; 5];
    let mut vz = [0.0; 5];
    let mut m = [0.0; 5];
    push5(&mut x, [0.0, 4.84143144246472090, -8.34336671824457987, 12.8943695621399930, -15.1111514016986312]);
    push5(&mut y, [0.0, -1.33081745316873100, 4.12401084012922153, -15.1111514016986312, -2.23307578883923100]);
    push5(&mut z, [0.0, -1.01285558609590400, -0.25201944206821800, -0.30550644688493600, 4.87198428709807900]);
    push5(&mut vx, [0.0, 0.00166007664274403690, 0.00110052230769298880, -0.000298068015449799380, 0.000276689588924791380]);
    push5(&mut vy, [0.0, -0.00276742510726862411, -0.00412401084012922153, -0.000736407576782031450, -0.000599815228414248880]);
    push5(&mut vz, [0.0, -0.00138340197747227880, -0.000618624084271047990, -0.000297654262186052250, -0.000038256625988509985]);
    push5(&mut m, [1.0, 0.000954791938424326609, 0.000285885980666130812, 0.0000436624404335156298, 0.0000515138902046611451]);
    offset_momentum(&x, &y, &z, &mut vx, &mut vy, &mut vz, &m);
    let mut s = 0;
    while s < 100000 {
        advance(&mut x, &mut y, &mut z, &mut vx, &mut vy, &mut vz, &m, 0.01);
        s += 1;
    }
    let e = energy(&x, &y, &z, &vx, &vy, &vz, &m);
    println!("nbody checksum = {}", (e * 1000000000.0) as i64);
}
