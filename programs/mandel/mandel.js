const n = 400;
const limit = 1000;
let total = 0;
for (let y = 0; y < n; y++) {
    const ci = -1.5 + y * (3.0 / n);
    for (let x = 0; x < n; x++) {
        const cr = -2.0 + x * (3.0 / n);
        let zr = 0.0, zi = 0.0;
        let iter = 0;
        while (zr * zr + zi * zi <= 4.0 && iter < limit) {
            const tr = zr * zr - zi * zi + cr;
            zi = 2.0 * zr * zi + ci;
            zr = tr;
            iter++;
        }
        total += iter;
    }
}
console.log("mandel " + n + " total = " + total);
