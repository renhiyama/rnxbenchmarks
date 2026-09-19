void main() {
  const n = 400;
  const limit = 1000;
  var total = 0;
  var y = 0;
  while (y < n) {
    final ci = -1.5 + y * (3.0 / n);
    var x = 0;
    while (x < n) {
      final cr = -2.0 + x * (3.0 / n);
      var zr = 0.0;
      var zi = 0.0;
      var iter = 0;
      while (zr * zr + zi * zi <= 4.0 && iter < limit) {
        final tr = zr * zr - zi * zi + cr;
        zi = 2.0 * zr * zi + ci;
        zr = tr;
        iter++;
      }
      total += iter;
      x++;
    }
    y++;
  }
  print("mandel $n total = $total");
}
