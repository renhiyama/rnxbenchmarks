const n = 256;
const nn = n * n;
const a = new Array(nn), b = new Array(nn), c = new Array(nn).fill(0);
for (let i = 0; i < nn; i++) {
    const r = Math.trunc(i / n);
    const col = i - r * n;
    a[i] = ((r * 7 + col * 13) % 16) - 8;
    b[i] = ((r * 13 - col * 7) % 16) - 8;
}
for (let r = 0; r < n; r++) {
    for (let k = 0; k < n; k++) {
        const aik = a[r * n + k];
        for (let j = 0; j < n; j++) {
            c[r * n + j] += aik * b[k * n + j];
        }
    }
}
let sum = 0;
for (let q = 0; q < nn; q++) sum += c[q];
console.log("matmul checksum = " + sum);
