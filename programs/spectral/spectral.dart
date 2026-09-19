double evalA(int i, int j) {
  final ij = i + j;
  return 1.0 / (((ij * (ij + 1) ~/ 2) + i + 1).toDouble());
}

void timesAv(List<double> v, List<double> out, int n) {
  var i = 0;
  while (i < n) {
    var s = 0.0;
    var j = 0;
    while (j < n) {
      s += evalA(i, j) * v[j];
      j++;
    }
    out[i] = s;
    i++;
  }
}

void timesA(List<double> v, List<double> out, int n) {
  var i = 0;
  while (i < n) {
    var s = 0.0;
    var j = 0;
    while (j < n) {
      s += evalA(j, i) * v[j];
      j++;
    }
    out[i] = s;
    i++;
  }
}

void main() {
  const n = 300;
  final u = List<double>.filled(n, 1.0);
  final v = List<double>.filled(n, 0.0);
  final w = List<double>.filled(n, 0.0);
  var it = 0;
  while (it < 10) {
    timesAv(u, w, n);
    timesA(w, v, n);
    timesAv(v, w, n);
    timesA(w, u, n);
    it++;
  }
  var vbv = 0.0;
  var vv = 0.0;
  var k = 0;
  while (k < n) {
    vbv += u[k] * v[k];
    vv += v[k] * v[k];
    k++;
  }
  print("spectral checksum = ${(vbv / vv * 1000000.0).toInt()}");
}
