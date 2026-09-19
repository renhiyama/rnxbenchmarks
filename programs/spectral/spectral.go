package main

import "fmt"

func evalA(i, j int) float64 {
    ij := i + j
    return 1.0 / float64((ij*(ij+1)/2)+i+1)
}

func timesAv(v, out []float64, n int) {
    for i := 0; i < n; i++ {
        s := 0.0
        for j := 0; j < n; j++ {
            s += evalA(i, j) * v[j]
        }
        out[i] = s
    }
}

func timesA(v, out []float64, n int) {
    for i := 0; i < n; i++ {
        s := 0.0
        for j := 0; j < n; j++ {
            s += evalA(j, i) * v[j]
        }
        out[i] = s
    }
}

func main() {
    n := 300
    u := make([]float64, n)
    v := make([]float64, n)
    w := make([]float64, n)
    for i := 0; i < n; i++ {
        u[i] = 1.0
    }
    for it := 0; it < 10; it++ {
        timesAv(u, w, n)
        timesA(w, v, n)
        timesAv(v, w, n)
        timesA(w, u, n)
    }
    vbv, vv := 0.0, 0.0
    for k := 0; k < n; k++ {
        vbv += u[k] * v[k]
        vv += v[k] * v[k]
    }
    fmt.Printf("spectral checksum = %d\n", int64(vbv/vv*1000000.0))
}
