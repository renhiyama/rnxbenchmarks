function evalA(i, j) {
    const ij = i + j;
    return 1.0 / (((ij * (ij + 1) / 2) | 0) + i + 1);
}

function timesAv(v, out, n) {
    for (let i = 0; i < n; i++) {
        let s = 0.0;
        for (let j = 0; j < n; j++) s += evalA(i, j) * v[j];
        out[i] = s;
    }
}

function timesA(v, out, n) {
    for (let i = 0; i < n; i++) {
        let s = 0.0;
        for (let j = 0; j < n; j++) s += evalA(j, i) * v[j];
        out[i] = s;
    }
}

const n = 300;
const u = new Array(n).fill(1.0);
const v = new Array(n).fill(0.0);
const w = new Array(n).fill(0.0);
for (let it = 0; it < 10; it++) {
    timesAv(u, w, n);
    timesA(w, v, n);
    timesAv(v, w, n);
    timesA(w, u, n);
}
let vbv = 0.0, vv = 0.0;
for (let k = 0; k < n; k++) { vbv += u[k] * v[k]; vv += v[k] * v[k]; }
console.log("spectral checksum = " + Math.trunc(vbv / vv * 1000000.0));
