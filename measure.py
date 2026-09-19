#!/usr/bin/env python3
"""Build and measure every benchmark program in every language.

Metrics per program x language: wall time (median of timed runs after
warmup), peak RSS (VmHWM polling), artifact size, and checksum match.
Writes RESULTS.md. Skips languages whose toolchain is missing.
"""

import json
import os
import shutil
import statistics
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(ROOT, "programs")
RUNS = os.path.join(ROOT, "runs")
RNX = os.environ.get("RNX_BIN", "/home/ren/coding/Rasmalai/compiler/target/debug/rnx")
GO = os.environ.get("GO_BIN", os.path.expanduser("~/tools/go/bin/go"))
JAVAC = os.environ.get("JAVAC_BIN", os.path.expanduser("~/tools/jdk/bin/javac"))
JAVA = os.environ.get("JAVA_BIN", os.path.expanduser("~/tools/jdk/bin/java"))

PROGRAMS = ["fib", "mandel", "nbody", "spectral", "matmul"]
EXPECTED = {
    "fib": "fib(35) = 9227465",
    "mandel": "mandel 400 total = 27654979",
    "nbody": "nbody checksum = 1516028815",
    "spectral": "spectral checksum = 1623646",
    "matmul": "matmul checksum = 38187008",
}
WARMUPS = 2
TIMED = 5


def have(cmd):
    return shutil.which(cmd) is not None


def version(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        out = (p.stdout + p.stderr).strip().splitlines()
        return out[0] if out else "?"
    except Exception as e:
        return f"missing ({e})"


def peak_rss_kb(pid, stop):
    peak = 0
    path = f"/proc/{pid}/status"
    while not stop.is_set():
        try:
            with open(path) as f:
                for line in f:
                    if line.startswith("VmHWM:"):
                        peak = max(peak, int(line.split()[1]))
                        break
        except Exception:
            pass
        time.sleep(0.002)
    try:
        with open(path) as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    peak = max(peak, int(line.split()[1]))
                    break
    except Exception:
        pass
    return peak


def run_timed(argv, cwd=None):
    """Returns (seconds, peak_rss_kb, stdout)."""
    stop = threading.Event()
    peak = [0]
    t0 = time.perf_counter()
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, cwd=cwd)

    def watch():
        peak[0] = peak_rss_kb(p.pid, stop)

    th = threading.Thread(target=watch, daemon=True)
    th.start()
    out, _ = p.communicate()
    dt = time.perf_counter() - t0
    stop.set()
    th.join(timeout=5)
    if p.returncode != 0:
        raise RuntimeError(f"{' '.join(argv)} exited {p.returncode}: {out[:200]}")
    return dt, peak[0], out.strip().splitlines()


def measure(argv, cwd=None):
    for _ in range(WARMUPS):
        run_timed(argv, cwd)
    times, peaks, lines = [], [], None
    for _ in range(TIMED):
        dt, rss, lines = run_timed(argv, cwd)
        times.append(dt)
        peaks.append(rss)
    return statistics.median(times), min(times), max(peaks), lines


LANGS = {}


def lang(name, build=None, run=None, size=None, ver=None):
    LANGS[name] = {"build": build, "run": run, "size": size, "ver": ver}


def exe(prog, tag):
    return os.path.join(RUNS, f"{prog}-{tag}")


def build_rnx(dev):
    tag = "rnx-dev" if dev else "rnx-rel"
    flag = [] if dev else ["--release"]

    def build(prog):
        src = os.path.join(PROG, prog, f"{prog}.rnx")
        subprocess.run([RNX, "build"] + flag + ["-o", exe(prog, tag), src],
                       check=True, capture_output=True, text=True)

    def run(prog):
        return [exe(prog, tag)]

    def size(prog):
        return os.path.getsize(exe(prog, tag))

    return build, run, size


b, r, s = build_rnx(True)
lang("rasmalai-dev", b, r, s, ["rnx", "workspace build (LLVM dev profile)"])
b, r, s = build_rnx(False)
lang("rasmalai-rel", b, r, s, ["rnx", "workspace build (LLVM O3 release)"])

if have("gcc"):
    def build(prog):
        subprocess.run(["gcc", "-O2", "-o", exe(prog, "c"),
                        os.path.join(PROG, prog, f"{prog}.c"), "-lm"],
                       check=True, capture_output=True, text=True)
    lang("c", build, lambda p: [exe(p, "c")],
         lambda p: os.path.getsize(exe(p, "c")), ["gcc", version(["gcc", "--version"])])
if have("g++"):
    def build(prog):
        subprocess.run(["g++", "-O2", "-o", exe(prog, "cpp"),
                        os.path.join(PROG, prog, f"{prog}.cpp"), "-lm"],
                       check=True, capture_output=True, text=True)
    lang("cpp", build, lambda p: [exe(p, "cpp")],
         lambda p: os.path.getsize(exe(p, "cpp")), ["g++", version(["g++", "--version"])])
if have("rustc"):
    def build(prog):
        subprocess.run(["rustc", "-O", "-o", exe(prog, "rs"),
                        os.path.join(PROG, prog, f"{prog}.rs")],
                       check=True, capture_output=True, text=True)
    lang("rust", build, lambda p: [exe(p, "rs")],
         lambda p: os.path.getsize(exe(p, "rs")), ["rustc", version(["rustc", "--version"])])
if have("node"):
    lang("node", None, lambda p: ["node", os.path.join(PROG, p, f"{p}.js")],
         lambda p: os.path.getsize(os.path.join(PROG, p, f"{p}.js")),
         ["node", version(["node", "--version"])])
if os.path.exists(GO):
    def build(prog):
        subprocess.run([GO, "build", "-o", exe(prog, "go"),
                        os.path.join(PROG, prog, f"{prog}.go")],
                       check=True, capture_output=True, text=True,
                       env={**os.environ, "GOFLAGS": "-mod=mod", "GOTOOLCHAIN": "local"})
    lang("go", build, lambda p: [exe(p, "go")],
         lambda p: os.path.getsize(exe(p, "go")), ["go", version([GO, "version"])])
if os.path.exists(JAVAC):
    NAMES = {"fib": "Fib", "mandel": "Mandel", "nbody": "Nbody",
             "spectral": "Spectral", "matmul": "Matmul"}

    def build(prog):
        subprocess.run([JAVAC, "-d", RUNS, os.path.join(PROG, prog, f"{NAMES[prog]}.java")],
                       check=True, capture_output=True, text=True)

    def run(prog):
        return [JAVA, "-cp", RUNS, NAMES[prog]]

    def size(prog):
        return os.path.getsize(os.path.join(RUNS, f"{NAMES[prog]}.class"))

    lang("java", build, run, size, ["javac", version([JAVAC, "-version"])])
if have("dart"):
    def build(prog):
        subprocess.run(["dart", "compile", "exe",
                        os.path.join(PROG, prog, f"{prog}.dart"),
                        "-o", exe(prog, "dart")],
                       check=True, capture_output=True, text=True)
    lang("dart", build, lambda p: [exe(p, "dart")],
         lambda p: os.path.getsize(exe(p, "dart")), ["dart", version(["dart", "--version"])])


def main():
    os.makedirs(RUNS, exist_ok=True)
    results = {"versions": {}, "programs": {}, "meta": machine_meta()}
    for name, spec in LANGS.items():
        v = spec["ver"]
        results["versions"][name] = f"{v[0]}: {v[1]}" if v else name
    print(f"languages: {sorted(LANGS)}", flush=True)
    for prog in PROGRAMS:
        results["programs"][prog] = {}
        print(f"== {prog} (expected: {EXPECTED[prog]})", flush=True)
        for name, spec in LANGS.items():
            try:
                if spec["build"]:
                    t0 = time.perf_counter()
                    spec["build"](prog)
                    build_s = time.perf_counter() - t0
                else:
                    build_s = 0.0
                med, best, rss, lines = measure(spec["run"](prog))
                ok = EXPECTED[prog] in lines
                size = spec["size"](prog) if spec["size"] else 0
                status = "OK " if ok else "MISMATCH"
                print(f"  [{status}] {name:14s} med={med:8.3f}s best={best:8.3f}s "
                      f"rss={rss:>8d}kB size={size:>9d}B build={build_s:6.1f}s", flush=True)
                results["programs"][prog][name] = {
                    "median_s": round(med, 4), "best_s": round(best, 4),
                    "peak_rss_kb": rss, "size_b": size,
                    "build_s": round(build_s, 1), "checksum_ok": ok,
                }
            except Exception as e:
                print(f"  [FAIL] {name:14s} {e}", flush=True)
                results["programs"][prog][name] = {"error": str(e)[:200]}
    with open(os.path.join(ROOT, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    write_md(results)


def machine_meta():
    import platform
    meta = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or platform.machine(),
        "python": platform.python_version(),
    }
    for path in ("/proc/cpuinfo",):
        try:
            with open(path) as f:
                for line in f:
                    if line.startswith("model name"):
                        meta["cpu"] = line.split(":", 1)[1].strip()
                        break
        except OSError:
            pass
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    meta["mem_kb"] = int(line.split()[1])
                    break
    except OSError:
        pass
    return meta


def human_size(b):
    for unit in ["B", "KB", "MB"]:
        if b < 1024 or unit == "MB":
            return f"{b:.0f}{unit}" if unit == "B" else f"{b:.1f}{unit}"
        b /= 1024.0
    return f"{b:.1f}GB"


def write_md(results):
    names = list(LANGS)
    L = []
    L.append("# Benchmark results")
    L.append("")
    meta = results.get("meta", {})
    L.append(f"Generated {meta.get('generated_at', '?')} on {meta.get('cpu', meta.get('machine', '?'))} "
             f"({meta.get('system', '?')} {meta.get('release', '')} {meta.get('machine', '')}).".rstrip())
    L.append("")
    L.append("Median wall time of 5 runs after 2 warmups, peak RSS (VmHWM),")
    L.append("artifact size, and checksum agreement. Build flags: gcc/g++ -O2,")
    L.append("rustc -O, go build, javac/java (Temurin 25), dart compile exe,")
    L.append("rnx build (dev) and rnx build --release.")
    L.append("")
    L.append("## Toolchains")
    L.append("")
    for n in names:
        L.append(f"- {results['versions'][n]}")
    L.append("")
    for prog in PROGRAMS:
        L.append(f"## {prog} (expected `{EXPECTED[prog]}`)")
        L.append("")
        L.append("| lang | median | best | peak RSS | size | checksum |")
        L.append("|---|---|---|---|---|---|")
        for n in names:
            r = results["programs"][prog].get(n, {})
            if "error" in r:
                L.append(f"| {n} | FAIL | | | | {r['error'][:60]} |")
                continue
            ok = "match" if r["checksum_ok"] else "MISMATCH"
            L.append(f"| {n} | {r['median_s']:.3f}s | {r['best_s']:.3f}s | "
                     f"{r['peak_rss_kb'] / 1024:.1f}MB | {human_size(r['size_b'])} | {ok} |")
        L.append("")
    with open(os.path.join(ROOT, "RESULTS.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("wrote RESULTS.md + results.json", flush=True)


if __name__ == "__main__":
    sys.exit(main())
