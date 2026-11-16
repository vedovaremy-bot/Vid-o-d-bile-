"""Génère la voix off (Piper, voix FR masculine), les timings mot par mot,
une petite musique de fond et les bruitages -> audio_mix.wav + timings.json"""
import json, os, re, wave, io, sys
import numpy as np
from piper import PiperVoice, SynthesisConfig

VOICE = os.environ.get("PIPER_VOICE", "voice/fr_FR-tom-medium.onnx")
SPEED = float(os.environ.get("LENGTH_SCALE", "0.86"))   # <1 = plus rapide
SR_OUT = 44100

script = json.load(open("script.json", encoding="utf-8"))
voice = PiperVoice.load(VOICE)
SR = voice.config.sample_rate

def synth(text):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        voice.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=SPEED))
    buf.seek(0)
    with wave.open(buf) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    # coupe les silences au début / fin
    thr = 0.012
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx): a = a[max(0, idx[0]-int(.02*SR)): idx[-1]+int(.04*SR)]
    return a

def clauses(text):
    # découpe en propositions sur la ponctuation, en gardant la ponctuation
    parts = re.findall(r'[^.,!?:…]+(?:\.\.\.|[.,!?:…])*', text)
    return [p.strip() for p in parts if p.strip()]

def pause_after(cl):
    if cl.endswith("..."): return 0.45
    if cl.endswith((".", "!", "?")): return 0.28
    if cl.endswith(":"): return 0.22
    return 0.12

audio = [np.zeros(int(0.15*SR), np.float32)]
t = 0.15
segs = []
for si, seg in enumerate(script["segments"]):
    s_start = t
    words = []
    txt = re.sub(r'((?:\.\.\.|[.,!?:…])+)\*', r'*\1', seg["text"])
    for cl in clauses(txt):
        clean = cl.replace("*", "")
        if not re.search(r"\w", clean): continue
        a = synth(clean)
        dur = len(a) / SR
        toks = cl.split()
        weights = [len(w.replace("*", "")) + 2 for w in toks]
        tot = sum(weights); acc = 0
        for w, wt in zip(toks, weights):
            words.append({"w": w, "s": round(t + dur*acc/tot, 3), "e": round(t + dur*(acc+wt)/tot, 3)})
            acc += wt
        audio.append(a); t += dur
        p = pause_after(clean)
        audio.append(np.zeros(int(p*SR), np.float32)); t += p
    segs.append({"scene": seg["scene"], "start": round(s_start, 3), "end": round(t, 3), "words": words})

voice_track = np.concatenate(audio)
# rééchantillonnage simple vers 44.1k
n_out = int(len(voice_track) * SR_OUT / SR)
voice_track = np.interp(np.linspace(0, len(voice_track)-1, n_out), np.arange(len(voice_track)), voice_track)
total = len(voice_track) / SR_OUT + 1.2

# hook "sur-merge" du marqueur *mot* -> chaque mot garde ses astérisques pour le surlignage
# fusion des mots *À vie.* sur plusieurs tokens
for s in segs:
    inside = False
    for w in s["words"]:
        raw = w["w"]
        starts, ends = raw.startswith("*"), raw.rstrip(".,!?:…").endswith("*")
        w["hl"] = inside or starts
        if starts and not ends: inside = True
        if ends: inside = False
        w["w"] = raw.replace("*", "")

# ---------- musique de fond (pizzicato Karplus-Strong + basse + charleston) ----------
rng = np.random.default_rng(3)
def pluck(freq, dur, sr=SR_OUT, decay=0.996):
    n = int(sr*dur); p = int(sr/freq)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i+1) % p])
    return out
def note(m): return 440 * 2**((m-69)/12)
bpm = 112; beat = 60/bpm; step = beat/2
music = np.zeros(int(total*SR_OUT)+SR_OUT)
prog = [[60,64,67,72],[57,60,64,69],[53,57,60,65],[55,59,62,67]]  # C Am F G
cache = {}
def add(sig, t0, gain):
    i = int(t0*SR_OUT); j = min(len(music), i+len(sig))
    if i < len(music): music[i:j] += sig[:j-i]*gain
pattern = [0,2,1,3,2,1,3,2]
nsteps = int(total/step)+1
for k in range(nsteps):
    bar = (k//8) % 4; chord = prog[bar]; t0 = k*step
    m = chord[pattern[k % 8]] + 12
    if m not in cache: cache[m] = pluck(note(m), 0.5)
    add(cache[m], t0, 0.22 if k % 2 == 0 else 0.15)
    if k % 4 == 0:
        b = chord[0]-24
        if ("b", b) not in cache: cache[("b", b)] = pluck(note(b), 0.9, decay=0.998)
        add(cache[("b", b)], t0, 0.35)
    # charleston léger
    hh = rng.normal(0, 1, int(0.03*SR_OUT)) * np.exp(-np.linspace(0, 8, int(0.03*SR_OUT)))
    hh = np.diff(hh, prepend=0)
    add(hh, t0, 0.05 if k % 2 else 0.025)
music = music[:int(total*SR_OUT)]
music /= (np.abs(music).max() + 1e-9)

# ---------- bruitages ----------
def whoosh(d=0.35):
    n = int(d*SR_OUT); x = rng.normal(0, 1, n)
    env = np.sin(np.linspace(0, np.pi, n))**2
    # passe-bas glissant
    y = np.zeros(n); a = np.linspace(0.02, 0.35, n); acc = 0
    for i in range(n): acc += a[i]*(x[i]-acc); y[i] = acc
    return y*env
def thud(d=0.4):
    n = int(d*SR_OUT); tt = np.arange(n)/SR_OUT
    f = 140*np.exp(-tt*9)+45
    return np.sin(2*np.pi*np.cumsum(f)/SR_OUT)*np.exp(-tt*10) + rng.normal(0,1,n)*np.exp(-tt*60)*0.4
def pop(d=0.12):
    n = int(d*SR_OUT); tt = np.arange(n)/SR_OUT
    f = 900*np.exp(-tt*25)+300
    return np.sin(2*np.pi*np.cumsum(f)/SR_OUT)*np.exp(-tt*30)

sfx = np.zeros_like(music)
def put(sig, t0, g):
    i = int(t0*SR_OUT); j = min(len(sfx), i+len(sig)); sfx[i:j] += sig[:j-i]*g
prev = None
for s in segs:
    if s["scene"] != prev and prev is not None: put(whoosh(), s["start"]-0.18, 0.5)
    prev = s["scene"]
for s in segs:
    for w in s["words"]:
        if w["w"].lower().startswith("coupable"): put(thud(), w["s"], 0.9); put(thud(), w["s"]-0.35, 0.6)
        if w["w"].lower().startswith("tribunal") and s["scene"] == "hook": put(thud(), w["s"], 0.7)
        if w["w"].lower().startswith("valise"): put(pop(), w["s"], 0.5)

vt = np.zeros_like(music); vt[:len(voice_track)] = voice_track[:len(vt)]
# ducking : musique plus basse quand la voix parle
env = np.convolve(np.abs(vt), np.ones(4410)/4410, mode="same")
duck = 1 - 0.55*np.clip(env*12, 0, 1)
mix = vt*1.0 + music*0.10*duck + sfx*0.35
mix /= max(1.0, np.abs(mix).max()/0.97)
pcm = (mix*32767).astype(np.int16)
with wave.open("audio_mix.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR_OUT); w.writeframes(pcm.tobytes())
json.dump({"duration": round(total, 3), "segments": segs}, open("timings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("durée totale: %.1fs" % total)
