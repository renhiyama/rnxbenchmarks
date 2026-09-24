# Benchmark results

Generated 2026-09-24T09:01:55Z on AMD Ryzen 7 8840HS w/ Radeon 780M Graphics (Linux 7.2.2-arch1-1 x86_64).

Median wall time of 5 runs after 2 warmups, peak RSS (VmHWM),
artifact size, and checksum agreement. Build flags: gcc/g++ -O2,
rustc -O, go build, javac/java (Temurin 25), dart compile exe,
rnx build (dev) and rnx build --release.

## Toolchains

- rnx: workspace build (LLVM dev profile)
- rnx: workspace build (LLVM O3 release)
- gcc: gcc (GCC) 16.2.1 20260810
- g++: g++ (GCC) 16.2.1 20260810
- rustc: rustc 1.98.1 (48a229cea 2026-09-01)
- node: v26.8.1
- go: go version go1.25.1 linux/amd64
- javac: javac 25.0.4.1
- dart: Dart SDK version: 3.13.2 (stable) (Tue Aug 25 01:01:12 2026 -0700) on "linux_x64"

## fib (expected `fib(35) = 9227465`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.057s | 0.057s | 3.3MB | 5.4MB | match |
| rasmalai-rel | 0.022s | 0.021s | 2.5MB | 402.1KB | match |
| c | 0.009s | 0.009s | 2.1MB | 15.6KB | match |
| cpp | 0.010s | 0.010s | 3.7MB | 15.6KB | match |
| rust | 0.018s | 0.017s | 2.2MB | 4.3MB | match |
| node | 0.102s | 0.096s | 54.4MB | 119B | match |
| go | 0.037s | 0.036s | 2.1MB | 2.2MB | match |
| java | 0.048s | 0.047s | 42.1MB | 977B | match |
| dart | 0.054s | 0.053s | 8.0MB | 6.2MB | match |

## mandel (expected `mandel 400 total = 27654979`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.279s | 0.277s | 2.9MB | 5.4MB | match |
| rasmalai-rel | 0.057s | 0.056s | 2.5MB | 402.8KB | match |
| c | 0.057s | 0.057s | 2.0MB | 15.6KB | match |
| cpp | 0.059s | 0.058s | 3.7MB | 15.6KB | match |
| rust | 0.057s | 0.056s | 2.2MB | 4.3MB | match |
| node | 0.093s | 0.086s | 56.1MB | 521B | match |
| go | 0.058s | 0.058s | 2.1MB | 2.2MB | match |
| java | 0.091s | 0.090s | 43.0MB | 1.2KB | match |
| dart | 0.059s | 0.058s | 7.9MB | 6.2MB | match |

## nbody (expected `nbody checksum = 1516028815`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.046s | 0.045s | 2.9MB | 5.4MB | match |
| rasmalai-rel | 0.007s | 0.006s | 2.5MB | 406.2KB | match |
| c | 0.006s | 0.006s | 2.0MB | 15.7KB | match |
| cpp | 0.007s | 0.007s | 3.7MB | 15.7KB | match |
| rust | 0.006s | 0.006s | 2.2MB | 4.3MB | match |
| node | 0.042s | 0.039s | 57.2MB | 2.7KB | match |
| go | 0.007s | 0.006s | 2.1MB | 2.2MB | match |
| java | 0.056s | 0.045s | 45.3MB | 2.6KB | match |
| dart | 0.016s | 0.014s | 10.6MB | 6.2MB | match |

## spectral (expected `spectral checksum = 1623646`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.031s | 0.030s | 3.0MB | 5.4MB | match |
| rasmalai-rel | 0.006s | 0.005s | 2.5MB | 404.4KB | match |
| c | 0.003s | 0.003s | 2.0MB | 15.8KB | match |
| cpp | 0.004s | 0.003s | 3.7MB | 16.3KB | match |
| rust | 0.005s | 0.005s | 2.2MB | 4.3MB | match |
| node | 0.039s | 0.036s | 58.4MB | 858B | match |
| go | 0.005s | 0.005s | 2.1MB | 2.2MB | match |
| java | 0.036s | 0.035s | 43.4MB | 1.5KB | match |
| dart | 0.017s | 0.017s | 11.4MB | 6.2MB | match |

## matmul (expected `matmul checksum = 38187008`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.063s | 0.062s | 4.5MB | 5.4MB | match |
| rasmalai-rel | 0.007s | 0.007s | 4.3MB | 403.4KB | match |
| c | 0.004s | 0.003s | 2.6MB | 15.7KB | match |
| cpp | 0.005s | 0.004s | 4.4MB | 16.2KB | match |
| rust | 0.007s | 0.007s | 3.7MB | 4.3MB | match |
| node | 0.054s | 0.054s | 62.3MB | 579B | match |
| go | 0.012s | 0.011s | 3.6MB | 2.2MB | match |
| java | 0.045s | 0.043s | 45.8MB | 1.2KB | match |
| dart | 0.032s | 0.031s | 9.3MB | 6.2MB | match |

