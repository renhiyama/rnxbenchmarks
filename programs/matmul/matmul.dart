void main() {
  const n = 256;
  final nn = n * n;
  final a = List<int>.filled(nn, 0);
  final b = List<int>.filled(nn, 0);
  final c = List<int>.filled(nn, 0);
  var i = 0;
  while (i < nn) {
    final r = i ~/ n;
    final col = i - r * n;
    a[i] = ((r * 7 + col * 13).remainder(16)) - 8;
    b[i] = ((r * 13 - col * 7).remainder(16)) - 8;
    i++;
  }
  var r = 0;
  while (r < n) {
    var k = 0;
    while (k < n) {
      final aik = a[r * n + k];
      var j = 0;
      while (j < n) {
        c[r * n + j] += aik * b[k * n + j];
        j++;
      }
      k++;
    }
    r++;
  }
  var sum = 0;
  var q = 0;
  while (q < nn) {
    sum += c[q];
    q++;
  }
  print("matmul checksum = $sum");
}
