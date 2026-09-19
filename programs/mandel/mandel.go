package main

import "fmt"

func main() {
    n := 400
    limit := 1000
    var total int64
    for y := 0; y < n; y++ {
        ci := -1.5 + float64(y)*(3.0/float64(n))
        for x := 0; x < n; x++ {
            cr := -2.0 + float64(x)*(3.0/float64(n))
            zr, zi := 0.0, 0.0
            iter := 0
            for zr*zr+zi*zi <= 4.0 && iter < limit {
                tr := zr*zr - zi*zi + cr
                zi = 2.0*zr*zi + ci
                zr = tr
                iter++
            }
            total += int64(iter)
        }
    }
    fmt.Printf("mandel %d total = %d\n", n, total)
}
