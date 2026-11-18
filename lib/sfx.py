"""Bibliothèque de bruitages synthétisés (aucun fichier externe).
Chaque fonction prend `dur` (secondes, pour les sons qui durent) et renvoie un tableau float mono à 44,1 kHz.
Utilisation dans script.json :
  "sfx": [{"word": "sonné", "type": "alarm", "dur": 4, "gain": 0.5},
          {"word": "retombe", "type": "land"},
          {"scene": "party", "at": 0.3, "type": "applause", "dur": 3}]
Clés optionnelles : n (n-ième occurrence du mot), offset (s), gain, repeat + gap, dur, ambient (true = baissé sous la voix).
"""
import numpy as np

SR = 44100
_rng = np.random.default_rng(7)


def _t(d):
    return np.arange(int(SR * d)) / SR


def _env(n, a=0.005, r=0.1):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr and nr < n: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def _lp(x, fc):
    k = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - k) * x[i] + k * acc; y[i] = acc
    return y


def _hp(x, fc):
    return x - _lp(x, fc)


def _noise(d):
    return _rng.normal(0, 1, int(SR * d))


def _norm(x, peak=0.9):
    m = np.abs(x).max()
    return x / m * peak if m > 0 else x


def _sweep(f0, f1, d, wave="sine"):
    t = _t(d); f = np.geomspace(f0, f1, len(t)) if f0 > 0 and f1 > 0 else np.linspace(f0, f1, len(t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    if wave == "square": return np.sign(np.sin(ph))
    if wave == "saw": return 2 * ((ph / (2 * np.pi)) % 1) - 1
    return np.sin(ph)


# ---------------------------------------------------------------- sons ponctuels
def pop(dur=0.12):
    t = _t(dur); return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t * 25) + 300) / SR) * np.exp(-t * 30)


def thud(dur=0.4):
    t = _t(dur); f = 140 * np.exp(-t * 9) + 45
    return _norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10) + _lp(_noise(dur), 900) * np.exp(-t * 40) * 2)


def land(dur=0.6):
    """quelqu'un/quelque chose qui retombe lourdement (boum + petits débris)"""
    x = thud(0.5) * 1.0
    deb = np.zeros(int(SR * dur))
    for i in range(6):
        p = int(SR * (0.08 + _rng.random() * 0.35)); n = int(SR * 0.03)
        if p + n < len(deb): deb[p:p + n] += _hp(_noise(0.03), 2000) * np.exp(-np.linspace(0, 6, n)) * 0.25
    deb[:len(x)] += x
    return _norm(deb)


def whoosh(dur=0.4):
    x = _noise(dur); n = len(x); y = np.empty(n); acc = 0; a = np.linspace(.02, .35, n)
    for i in range(n): acc += a[i] * (x[i] - acc); y[i] = acc
    return _norm(y * np.sin(np.linspace(0, np.pi, n)) ** 2, .8)


def jump(dur=0.35):
    """saut cartoon : 'bwoup' qui monte"""
    t = _t(dur); return _sweep(180, 900, dur) * np.exp(-t * 4) * _env(len(t), .005, .05)


def boing(dur=0.6):
    t = _t(dur); f = 220 + 120 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)


def fall_whistle(dur=1.0):
    """sifflement qui descend (chute)"""
    t = _t(dur); return 0.6 * _sweep(1800, 300, dur) * _env(len(t), .05, .1)


def knock(dur=0.15):
    t = _t(dur)
    return (np.sin(2 * np.pi * 180 * t) + .5 * np.sin(2 * np.pi * 420 * t)) * np.exp(-t * 45) + _noise(dur) * np.exp(-t * 120) * .5


def door_slam(dur=0.6):
    t = _t(dur); return _norm(thud(dur) + _lp(_noise(dur), 3000) * np.exp(-t * 30) * .6 + np.sin(2 * np.pi * 95 * t) * np.exp(-t * 6) * .5)


def creak(dur=0.8):
    t = _t(dur); f = 300 + 80 * np.sin(2 * np.pi * 1.3 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return _norm(np.sign(np.sin(ph)) * (0.5 + 0.5 * np.sin(2 * np.pi * 37 * t)) * _env(len(t), .05, .2), .5)


def splash(dur=0.9):
    t = _t(dur); x = _lp(_noise(dur), 2500) * np.exp(-t * 6) + _hp(_noise(dur), 4000) * np.exp(-t * 12) * .4
    for i in range(10):  # gouttes
        p = int(SR * (0.15 + _rng.random() * 0.6)); n = int(SR * 0.05)
        if p + n < len(x): x[p:p + n] += np.sin(2 * np.pi * np.cumsum(np.linspace(900, 1600, n)) / SR) * np.exp(-np.linspace(0, 8, n)) * .3
    return _norm(x)


def bubbles(dur=1.5):
    x = np.zeros(int(SR * dur))
    for i in range(int(dur * 9)):
        p = int(_rng.random() * (len(x) - SR * .08)); n = int(SR * .06); f0 = 300 + _rng.random() * 500
        x[p:p + n] += np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f0 * 2.2, n)) / SR) * np.exp(-np.linspace(0, 5, n))
    return _norm(x, .6)


def glass(dur=0.8):
    t = _t(dur); x = _hp(_noise(dur), 3000) * np.exp(-t * 15)
    for f in [2400, 3100, 3900, 4700, 5600]: x += np.sin(2 * np.pi * f * t + _rng.random() * 6) * np.exp(-t * (6 + _rng.random() * 8)) * .25
    return _norm(x)


def crack(dur=0.25):
    t = _t(dur); return _noise(dur) * np.exp(-t * 25) * (_rng.random(len(t)) > .7)


def honk(dur=0.5):
    t = _t(dur); x = np.sign(np.sin(2 * np.pi * 350 * t)) + np.sign(np.sin(2 * np.pi * 440 * t))
    return _norm(_lp(x, 2500) * _env(len(t), .01, .05), .6)


def ding(dur=1.2):
    t = _t(dur); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) * a for f, d, a in [(1320, 3, 1), (2640, 5, .4), (3960, 8, .2)]) * .6


def cash(dur=1.0):
    x = np.zeros(int(SR * dur)); d = ding(0.9); x[int(.15 * SR):int(.15 * SR) + len(d)] += d[:len(x) - int(.15 * SR)]
    for i in range(8):
        p = int(_rng.random() * .15 * SR); n = int(.02 * SR); x[p:p + n] += _hp(_noise(.02), 3000) * .4
    return _norm(x)


def explosion(dur=1.8):
    t = _t(dur); return _norm(_lp(_noise(dur), 400) * np.exp(-t * 2.5) * 3 + np.sin(2 * np.pi * 50 * t) * np.exp(-t * 3) + _noise(dur) * np.exp(-t * 20) * .5)


def fart(dur=0.7):
    t = _t(dur); f = 90 + 40 * np.sin(2 * np.pi * 7 * t) + _rng.normal(0, 8, len(t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return _norm(_lp(np.sign(np.sin(ph)) * (0.6 + 0.4 * _rng.random(len(t))), 700) * _env(len(t), .02, .15), .7)


def magic(dur=1.0):
    x = np.zeros(int(SR * dur))
    for i, f in enumerate([1047, 1319, 1568, 2093, 2637, 3136]):
        p = int(i * .07 * SR)
        tone = np.sin(2 * np.pi * f * _t(.5)) * np.exp(-_t(.5) * 7)
        if p + len(tone) < len(x): x[p:p + len(tone)] += tone
    return _norm(x, .6)


def sad_trombone(dur=2.2):
    """'wah wah wah waaah' de l'échec"""
    x = np.zeros(int(SR * dur)); notes = [(311, .45), (294, .45), (277, .45), (262, .85)]; p = 0
    for i, (f, d) in enumerate(notes):
        t = _t(d); vib = 1 + (0.03 * np.sin(2 * np.pi * 6 * t) if i == 3 else 0)
        s = _lp(_sweep(f * 1.02, f * .98, d, "saw") * vib, 1400) * _env(len(t), .03, .08)
        n = int(SR * d); x[p:p + n] += s[:len(x) - p]; p += n
    return _norm(x, .7)


def gulp(dur=0.3):
    t = _t(dur); return np.sin(2 * np.pi * np.cumsum(np.linspace(500, 150, len(t))) / SR) * np.exp(-((t - .1) ** 2) / .003)


def crunch(dur=0.4):
    x = np.zeros(int(SR * dur))
    for i in range(14):
        p = int(_rng.random() * (len(x) - 800)); n = 600; x[p:p + n] += _hp(_noise(n / SR), 1500) * np.exp(-np.linspace(0, 6, n))
    return _norm(x, .7)


def punch(dur=0.35):
    t = _t(dur); return _norm(thud(dur) * .8 + _lp(_noise(dur), 2000) * np.exp(-t * 35))


def zip_(dur=0.3):
    return _norm(_hp(_noise(dur), 2500) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * np.cumsum(np.linspace(30, 90, int(SR * dur))) / SR))) * _env(int(SR * dur), .01, .05), .6)


# ---------------------------------------------------------------- sons qui durent (dur)
def alarm(dur=3.0):
    """réveil mécanique : marteau sur deux cloches, très rapide"""
    t = _t(dur); x = np.zeros_like(t); step = 1 / 22
    for k in range(int(dur / step)):
        p = int(k * step * SR); n = int(min(.12, dur - k * step) * SR)
        if n <= 0: break
        tt = np.arange(n) / SR; f = 2350 if k % 2 else 2650
        x[p:p + n] += (np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt * 40)
    return _norm(x * _env(len(t), .005, .05), .7)


def alarm_muffled(dur=3.0):
    return _norm(_lp(alarm(dur), 700), .6)


def phone_ring(dur=3.0):
    t = _t(dur); on = ((t % 2.0) < 1.0).astype(float) * ((t * 20 % 1) < .5)
    return _norm((np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * _lp(on, 200), .6)


def siren(dur=3.0):
    t = _t(dur); f = 750 + 350 * np.sin(2 * np.pi * .5 * t)
    return _norm(_lp(_sweep(1, 1, dur) * 0 + np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)), 3000) * _env(len(t), .2, .3), .5)


def footsteps(dur=2.0, rate=2.2):
    x = np.zeros(int(SR * dur)); k = 0
    while True:
        p = int(k / rate * SR)
        if p >= len(x): break
        s = _lp(_noise(.08), 600 + 300 * (k % 2)) * np.exp(-np.linspace(0, 9, int(.08 * SR)))
        x[p:p + len(s)] += s[:len(x) - p]; k += 1
    return _norm(x, .7)


def run(dur=1.5):
    return footsteps(dur, 5.5)


def applause(dur=3.0):
    x = np.zeros(int(SR * dur)); n = int(dur * 220)
    for i in range(n):
        p = int(_rng.random() * (len(x) - 500)); c = _hp(_noise(.01), 1200) * np.exp(-np.linspace(0, 8, int(.01 * SR)))
        x[p:p + len(c)] += c * (.5 + _rng.random() * .5)
    return _norm(x * _env(len(x), .3, .6), .6)


def snore(dur=3.0):
    t = _t(dur); cyc = np.clip(np.sin(2 * np.pi * .4 * t), 0, 1) ** 2
    return _norm(_lp(_noise(dur) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 70 * t))), 500) * cyc, .6)


def tick(dur=3.0):
    x = np.zeros(int(SR * dur))
    for k in range(int(dur * 2)):
        p = int(k * .5 * SR); c = _hp(_noise(.006), 2000) * (1 if k % 2 else .7); x[p:p + len(c)] += c[:len(x) - p]
    return _norm(x, .5)


def rain(dur=3.0):
    return _norm(_hp(_lp(_noise(dur), 6000), 400) * _env(int(SR * dur), .4, .4), .4)


def wind(dur=3.0):
    t = _t(dur); return _norm(_lp(_noise(dur), 500) * (0.6 + 0.4 * np.sin(2 * np.pi * .3 * t)) * _env(len(t), .5, .5), .5)


def engine(dur=3.0):
    t = _t(dur); f = 45 + 10 * np.sin(2 * np.pi * .7 * t)
    return _norm(_lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) + _noise(dur) * .3, 400) * _env(len(t), .2, .3), .5)


def drumroll(dur=2.0):
    x = np.zeros(int(SR * dur)); k = 0
    while k / 28 < dur:
        p = int(k / 28 * SR); c = _lp(_noise(.04), 2500) * np.exp(-np.linspace(0, 7, int(.04 * SR))) * (.6 + .4 * k / (dur * 28))
        x[p:p + len(c)] += c[:len(x) - p]; k += 1
    return _norm(x, .7)


def birds(dur=3.0):
    x = np.zeros(int(SR * dur))
    for i in range(int(dur * 3)):
        p = int(_rng.random() * (len(x) - SR * .2)); d = .08 + _rng.random() * .1; f0 = 2500 + _rng.random() * 1500
        s = _sweep(f0, f0 * 1.4, d) * np.sin(np.linspace(0, np.pi, int(SR * d))); x[p:p + len(s)] += s
    return _norm(x, .4)


def crowd(dur=3.0):
    t = _t(dur); return _norm(_lp(_noise(dur), 900) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.7 * t)) * _env(len(t), .3, .5), .5)


def buzz(dur=2.0):
    """mouches qui volent"""
    t = _t(dur); f = 210 + 25 * np.sin(2 * np.pi * 3.1 * t) + 15 * np.sin(2 * np.pi * 7.3 * t)
    return _norm(_lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)), 1800) * (0.6 + 0.4 * np.sin(2 * np.pi * .9 * t) ** 2) * _env(len(t), .1, .2), .4)


def clank(dur=0.5):
    """épées / métal qui s'entrechoquent"""
    t = _t(dur); return _norm(sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dcy) for f, dcy in [(1800, 9), (2650, 12), (4100, 16), (5300, 20)]) + _hp(_noise(dur), 3000) * np.exp(-t * 60), .7)


def washer(dur=4.0):
    """machine à laver qui tourne (ronronnement + eau qui clapote)"""
    t = _t(dur); hum = _lp(np.sign(np.sin(2 * np.pi * 55 * t)), 300) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.2 * t))
    slosh = _lp(_noise(dur), 900) * (0.5 + 0.5 * np.sin(2 * np.pi * .8 * t) ** 2)
    return _norm((hum + slosh * 1.5) * _env(len(t), .3, .3), .55)


def shrink(dur=0.9):
    """rétrécissement cartoon (son qui descend en sautillant)"""
    t = _t(dur); f = np.geomspace(1400, 180, len(t)) * (1 + .15 * np.sign(np.sin(2 * np.pi * 18 * t)))
    return _norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), .01, .1), .6)


SFX = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_") and k not in ("np",)}
SFX["zip"] = zip_
LONG = {"alarm", "alarm_muffled", "phone_ring", "siren", "footsteps", "run", "applause", "snore", "tick", "rain", "wind",
        "engine", "drumroll", "birds", "crowd", "bubbles", "buzz", "washer"}
