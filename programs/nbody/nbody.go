package main

import (
    "fmt"
    "math"
)

func push5(a []float64, v0, v1, v2, v3, v4 float64) {
    a[0], a[1], a[2], a[3], a[4] = v0, v1, v2, v3, v4
}

func offsetMomentum(x, y, z, vx, vy, vz, m []float64) {
    px, py, pz := 0.0, 0.0, 0.0
    for i := 0; i < 5; i++ {
        px += vx[i] * m[i]
        py += vy[i] * m[i]
        pz += vz[i] * m[i]
    }
    vx[0] = 0.0 - px/1.0
    vy[0] = 0.0 - py/1.0
    vz[0] = 0.0 - pz/1.0
}

func advance(x, y, z, vx, vy, vz, m []float64, dt float64) {
    for i := 0; i < 5; i++ {
        for j := i + 1; j < 5; j++ {
            dx := x[i] - x[j]
            dy := y[i] - y[j]
            dz := z[i] - z[j]
            dsq := dx*dx + dy*dy + dz*dz
            dist := math.Sqrt(dsq)
            mag := dt / (dsq * dist)
            vx[i] -= dx * m[j] * mag
            vy[i] -= dy * m[j] * mag
            vz[i] -= dz * m[j] * mag
            vx[j] += dx * m[i] * mag
            vy[j] += dy * m[i] * mag
            vz[j] += dz * m[i] * mag
        }
    }
    for k := 0; k < 5; k++ {
        x[k] += dt * vx[k]
        y[k] += dt * vy[k]
        z[k] += dt * vz[k]
    }
}

func energy(x, y, z, vx, vy, vz, m []float64) float64 {
    e := 0.0
    for i := 0; i < 5; i++ {
        e += 0.5 * m[i] * (vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])
        for j := i + 1; j < 5; j++ {
            dx := x[i] - x[j]
            dy := y[i] - y[j]
            dz := z[i] - z[j]
            dist := math.Sqrt(dx*dx + dy*dy + dz*dz)
            e -= (m[i] * m[j]) / dist
        }
    }
    return e
}

func main() {
    x := make([]float64, 5)
    y := make([]float64, 5)
    z := make([]float64, 5)
    vx := make([]float64, 5)
    vy := make([]float64, 5)
    vz := make([]float64, 5)
    m := make([]float64, 5)
    push5(x, 0.0, 4.84143144246472090, -8.34336671824457987, 12.8943695621399930, -15.1111514016986312)
    push5(y, 0.0, -1.33081745316873100, 4.12401084012922153, -15.1111514016986312, -2.23307578883923100)
    push5(z, 0.0, -1.01285558609590400, -0.25201944206821800, -0.30550644688493600, 4.87198428709807900)
    push5(vx, 0.0, 0.00166007664274403690, 0.00110052230769298880, -0.000298068015449799380, 0.000276689588924791380)
    push5(vy, 0.0, -0.00276742510726862411, -0.00412401084012922153, -0.000736407576782031450, -0.000599815228414248880)
    push5(vz, 0.0, -0.00138340197747227880, -0.000618624084271047990, -0.000297654262186052250, -0.000038256625988509985)
    push5(m, 1.0, 0.000954791938424326609, 0.000285885980666130812, 0.0000436624404335156298, 0.0000515138902046611451)
    offsetMomentum(x, y, z, vx, vy, vz, m)
    for s := 0; s < 100000; s++ {
        advance(x, y, z, vx, vy, vz, m, 0.01)
    }
    e := energy(x, y, z, vx, vy, vz, m)
    fmt.Printf("nbody checksum = %d\n", int64(e*1000000000.0))
}
