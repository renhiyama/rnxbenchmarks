# Language benchmarks

Five classic programs, eight languages, one checksum each. Everything is
sized to finish in well under a second in C so the full matrix runs in
minutes. See RESULTS.md for numbers, results.json for raw data.

## Programs (all print an exact checksum line)

| Program | What it stresses | Size | Checksum |
|---|---|---|---|
| fib | naive recursion, call overhead | fib(35) | 9227465 |
| mandel | double float loops, branches | 400x400, 1000 iters | 27654979 |
| nbody | sqrt-heavy float arrays | 5 bodies, 100k steps | 1516028815 |
| spectral | array traversals, division | N=300, 10 iters | 1623646 |
| matmul | int arrays, bounds checks | 256x256 | 38187008 |

Float programs use IEEE-754 doubles with identical operation order, so
checksums agree bit-for-bit. Integer checksums print directly. Rasmalai
sources stay inside the portable subset (while loops, no ranges), which
is also why they run unchanged on the interpreter, Cranelift, and LLVM.

## Languages and builds

- rasmalai-dev: `rnx build` (LLVM dev profile)
- rasmalai-rel: `rnx build --release` (LLVM O3, stripped)
- c: `gcc -O2`, cpp: `g++ -O2`, rust: `rustc -O`
- node: `node file.js` (JIT, no build)
- go: `go build` (1.25.1, installed to ~/tools)
- java: `javac` + `java` (Temurin 25, installed to ~/tools)
- dart: `dart compile exe` (AOT)

Swift has no Linux toolchain in this environment, so it is not measured.
Go and Java toolchains were installed as user-local tarballs because the
system only shipped a JRE without javac.

## Method

`measure.py` builds everything into runs/, then per program x language
does 2 warmup runs plus 5 timed runs (median reported). Peak RSS comes
from polling VmHWM in /proc during the run. Artifact size is the binary
on disk (source bytes for node, .class bytes for java). Any checksum
mismatch or nonzero exit fails that cell loudly instead of recording a
number. Rerun any time with `python3 measure.py` (needs the same PATH:
rnx debug binary, go and jdk under ~/tools).

## Automation and consumers

`.github/workflows/bench.yml` reruns the full matrix on pushes that touch
`programs/` or `measure.py`, on the 1st of every month (04:00 UTC), and on
manual dispatch. It installs gcc, Rust, Node 24, Go 1.25, Temurin Java 25,
and stable Dart, builds `rnx` from the compiler repo, runs `measure.py`,
and commits the refreshed `results.json` + `RESULTS.md` back to main.

The compiler source comes from the `RASMALAI_REPO` / `RASMALAI_REF`
repository variables (default `renhiyama/Rasmalai@main`); local runs use
`RNX_BIN`, `GO_BIN`, `JAVAC_BIN`, and `JAVA_BIN` env overrides instead.

`results.json` is the machine-readable contract. Each run embeds `meta`
(machine, CPU, date) next to `versions` and per-program cells, and every
cell carries `checksum_ok`, so consumers can reject stale or broken runs.
The Rasmalai website pulls it verbatim:

```sh
node website/scripts/pull-benchmarks.mjs \
  https://raw.githubusercontent.com/renhiyama/rnxbenchmarks/main/results.json
```

which writes a slim snapshot plus provenance (`source_repo`, `fetched_at`,
`meta`) into `website/src/lib/benchmarks/results.json`. The homepage
renders medians straight from that snapshot and links back here.

## Reading the numbers

- rasmalai-rel ties C on mandel and nbody, lands ~2x behind on fib,
  spectral, and matmul (bounds-checked refcounted arrays vs raw
  pointers, closed from ~22x by bounds-check promotion plus inline
  element access with TBAA-tagged header/payload splits). It beats
  node and java on every program, matches rust on nbody/spectral/
  matmul, and splits with dart and go.
- rasmalai-dev runs ~1.5-5x slower than release; it still takes fib
  and spectral off node, but trails node/java on the loop-heavy trio.
  Release strips binaries from 5.2MB to ~360KB.
- Native RSS sits at 2-4MB (go similar); node/java carry 40-60MB
  runtimes; dart exe ~8-11MB.
- Sub-0.1s cells include process startup; treat single-digit
  millisecond gaps as noise.
