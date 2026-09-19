# Benchmark results

Generated 2026-09-19T03:04:50Z on AMD Ryzen 7 8840HS w/ Radeon 780M Graphics (Linux 7.2.2-arch1-1 x86_64).

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
| rasmalai-dev | 0.083s | 0.081s | 2.7MB | 5.2MB | match |
| rasmalai-rel | 0.029s | 0.029s | 2.4MB | 356.1KB | match |
| c | 0.013s | 0.012s | 2.0MB | 15.6KB | match |
| cpp | 0.013s | 0.013s | 3.7MB | 15.6KB | match |
| rust | 0.025s | 0.024s | 2.2MB | 4.3MB | match |
| node | 0.137s | 0.134s | 54.8MB | 119B | match |
| go | 0.054s | 0.053s | 2.1MB | 2.2MB | match |
| java | 0.064s | 0.062s | 42.1MB | 977B | match |
| dart | 0.079s | 0.078s | 7.8MB | 6.2MB | match |

## mandel (expected `mandel 400 total = 27654979`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.401s | 0.397s | 2.8MB | 5.2MB | match |
| rasmalai-rel | 0.085s | 0.084s | 2.4MB | 356.9KB | match |
| c | 0.086s | 0.084s | 2.0MB | 15.6KB | match |
| cpp | 0.086s | 0.086s | 3.7MB | 15.6KB | match |
| rust | 0.085s | 0.082s | 2.2MB | 4.3MB | match |
| node | 0.127s | 0.126s | 56.2MB | 521B | match |
| go | 0.086s | 0.084s | 2.1MB | 2.2MB | match |
| java | 0.129s | 0.124s | 43.1MB | 1.2KB | match |
| dart | 0.086s | 0.085s | 8.1MB | 6.2MB | match |

## nbody (expected `nbody checksum = 1516028815`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.067s | 0.066s | 2.6MB | 5.2MB | match |
| rasmalai-rel | 0.009s | 0.009s | 2.5MB | 361.7KB | match |
| c | 0.008s | 0.008s | 2.0MB | 15.7KB | match |
| cpp | 0.010s | 0.009s | 3.7MB | 15.7KB | match |
| rust | 0.009s | 0.008s | 2.2MB | 4.3MB | match |
| node | 0.054s | 0.052s | 57.4MB | 2.7KB | match |
| go | 0.010s | 0.009s | 2.1MB | 2.2MB | match |
| java | 0.071s | 0.058s | 45.3MB | 2.6KB | match |
| dart | 0.023s | 0.021s | 10.3MB | 6.2MB | match |

## spectral (expected `spectral checksum = 1623646`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.045s | 0.043s | 2.7MB | 5.2MB | match |
| rasmalai-rel | 0.007s | 0.007s | 2.5MB | 359.9KB | match |
| c | 0.005s | 0.004s | 2.0MB | 15.8KB | match |
| cpp | 0.005s | 0.005s | 3.7MB | 16.3KB | match |
| rust | 0.006s | 0.006s | 2.2MB | 4.3MB | match |
| node | 0.050s | 0.043s | 57.9MB | 858B | match |
| go | 0.008s | 0.007s | 2.1MB | 2.2MB | match |
| java | 0.052s | 0.048s | 43.4MB | 1.5KB | match |
| dart | 0.024s | 0.022s | 11.4MB | 6.2MB | match |

## matmul (expected `matmul checksum = 38187008`)

| lang | median | best | peak RSS | size | checksum |
|---|---|---|---|---|---|
| rasmalai-dev | 0.093s | 0.092s | 4.4MB | 5.2MB | match |
| rasmalai-rel | 0.010s | 0.010s | 4.2MB | 358.9KB | match |
| c | 0.005s | 0.004s | 2.6MB | 15.7KB | match |
| cpp | 0.005s | 0.005s | 4.5MB | 16.2KB | match |
| rust | 0.009s | 0.008s | 3.6MB | 4.3MB | match |
| node | 0.073s | 0.069s | 62.3MB | 579B | match |
| go | 0.018s | 0.016s | 3.6MB | 2.2MB | match |
| java | 0.058s | 0.057s | 45.7MB | 1.2KB | match |
| dart | 0.046s | 0.044s | 9.6MB | 6.2MB | match |

