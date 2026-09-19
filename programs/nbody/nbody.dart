import 'dart:math' as math;

void push5(List<double> a, double v0, double v1, double v2, double v3, double v4) {
  a[0] = v0; a[1] = v1; a[2] = v2; a[3] = v3; a[4] = v4;
}

void offsetMomentum(List<double> x, List<double> y, List<double> z,
    List<double> vx, List<double> vy, List<double> vz, List<double> m) {
  var px = 0.0, py = 0.0, pz = 0.0;
  var i = 0;
  while (i < 5) {
    px += vx[i] * m[i];
    py += vy[i] * m[i];
    pz += vz[i] * m[i];
    i++;
  }
  vx[0] = 0.0 - px / 1.0;
  vy[0] = 0.0 - py / 1.0;
  vz[0] = 0.0 - pz / 1.0;
}

void advance(List<double> x, List<double> y, List<double> z,
    List<double> vx, List<double> vy, List<double> vz, List<double> m, double dt) {
  var i = 0;
  while (i < 5) {
    var j = i + 1;
    while (j < 5) {
      final dx = x[i] - x[j];
      final dy = y[i] - y[j];
      final dz = z[i] - z[j];
      final dsq = dx * dx + dy * dy + dz * dz;
      final dist = math.sqrt(dsq);
      final mag = dt / (dsq * dist);
      vx[i] -= dx * m[j] * mag;
      vy[i] -= dy * m[j] * mag;
      vz[i] -= dz * m[j] * mag;
      vx[j] += dx * m[i] * mag;
      vy[j] += dy * m[i] * mag;
      vz[j] += dz * m[i] * mag;
      j++;
    }
    i++;
  }
  var k = 0;
  while (k < 5) {
    x[k] += dt * vx[k];
    y[k] += dt * vy[k];
    z[k] += dt * vz[k];
    k++;
  }
}

double energy(List<double> x, List<double> y, List<double> z,
    List<double> vx, List<double> vy, List<double> vz, List<double> m) {
  var e = 0.0;
  var i = 0;
  while (i < 5) {
    e += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i]);
    var j = i + 1;
    while (j < 5) {
      final dx = x[i] - x[j];
      final dy = y[i] - y[j];
      final dz = z[i] - z[j];
      final dist = math.sqrt(dx * dx + dy * dy + dz * dz);
      e -= (m[i] * m[j]) / dist;
      j++;
    }
    i++;
  }
  return e;
}

void main() {
  final x = List<double>.filled(5, 0.0);
  final y = List<double>.filled(5, 0.0);
  final z = List<double>.filled(5, 0.0);
  final vx = List<double>.filled(5, 0.0);
  final vy = List<double>.filled(5, 0.0);
  final vz = List<double>.filled(5, 0.0);
  final m = List<double>.filled(5, 0.0);
  push5(x, 0.0, 4.84143144246472090, -8.34336671824457987, 12.8943695621399930, -15.1111514016986312);
  push5(y, 0.0, -1.33081745316873100, 4.12401084012922153, -15.1111514016986312, -2.23307578883923100);
  push5(z, 0.0, -1.01285558609590400, -0.25201944206821800, -0.30550644688493600, 4.87198428709807900);
  push5(vx, 0.0, 0.00166007664274403690, 0.00110052230769298880, -0.000298068015449799380, 0.000276689588924791380);
  push5(vy, 0.0, -0.00276742510726862411, -0.00412401084012922153, -0.000736407576782031450, -0.000599815228414248880);
  push5(vz, 0.0, -0.00138340197747227880, -0.000618624084271047990, -0.000297654262186052250, -0.000038256625988509985);
  push5(m, 1.0, 0.000954791938424326609, 0.000285885980666130812, 0.0000436624404335156298, 0.0000515138902046611451);
  offsetMomentum(x, y, z, vx, vy, vz, m);
  var s = 0;
  while (s < 100000) {
    advance(x, y, z, vx, vy, vz, m, 0.01);
    s++;
  }
  final e = energy(x, y, z, vx, vy, vz, m);
  print("nbody checksum = ${(e * 1000000000.0).toInt()}");
}
