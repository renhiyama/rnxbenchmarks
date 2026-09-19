package main

import "fmt"

func main() {
    n := 256
    nn := n * n
    a := make([]int64, nn)
    b := make([]int64, nn)
    c := make([]int64, nn)
    for i := 0; i < nn; i++ {
        r := int64(i / n)
        col := int64(i - int(r)*n)
        a[i] = ((r*7+col*13)%16) - 8
        b[i] = ((r*13-col*7)%16) - 8
    }
    for r := 0; r < n; r++ {
        for k := 0; k < n; k++ {
            aik := a[r*n+k]
            for j := 0; j < n; j++ {
                c[r*n+j] += aik * b[k*n+j]
            }
        }
    }
    var sum int64
    for q := 0; q < nn; q++ {
        sum += c[q]
    }
    fmt.Printf("matmul checksum = %d\n", sum)
}
