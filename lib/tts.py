"""Voix off + timings mot par mot + musique + bruitages.
Usage (depuis le dossier de la vidéo) : python3 ../lib/tts.py
Variables : ENGINE (piper|elevenlabs), VOICE (défaut fr_FR-tom-medium), EL_VOICE, EL_MODEL, SPEAKER, LENGTH_SCALE, NOISE, NOISE_W\nscript.json peut aussi contenir "engine": "elevenlabs" et "el_voice": "<voice_id>"
Les bruitages se déclarent dans script.json : "sfx": [{"word": "toc", "type": "knock"}, ...]"""
import json, os, re, subprocess, sys, tempfile, wave
import numpy as np
from piper import PiperVoice, SynthesisConfig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.environ.get("VOICE", "fr_FR-tom-medium")   # voix choisie par l'utilisateur (voix 1)
CFG = SynthesisConfig(
    speaker_id=int(os.environ["SPEAKER"]) if "SPEAKER" in os.environ else None,
    length_scale=float(os.environ.get("LENGTH_SCALE", "0.86")),
    noise_scale=float(os.environ.get("NOISE", "0.667")),     # + = intonation plus vivante
    noise_w_scale=float(os.environ.get("NOISE_W", "0.8")),  # + = rythme plus varié
)
SR_OUT = 44100
script = json.load(open("script.json", encoding="utf-8"))
ENGINE = os.environ.get("ENGINE", script.get("engine", "elevenlabs"))   # défaut : ElevenLabs (voix validée) ; "piper" = ancienne voix 1
EL_VOICE = os.environ.get("EL_VOICE", script.get("el_voice", "3Tp5mYhT9wrfnry9pzvV"))
EL_MODEL = os.environ.get("EL_MODEL", "eleven_multilingual_v2")
if ENGINE == "piper":
    voice = PiperVoice.load(os.path.join(ROOT, "voices", VOICE + ".onnx"))
    SR = voice.config.sample_rate
else:
    SR = 44100
rng = np.random.default_rng(3)

def trim(a, sr):
    idx = np.where(np.abs(a) > 0.012)[0]
    return a[max(0, idx[0]-int(.02*sr)): idx[-1]+int(.05*sr)] if len(idx) else a

def end_pause(sentence):
    s = sentence.rstrip("* ")
    if s.endswith(("...", "…")): return 0.50
    if s.endswith("?") or s.endswith("!"): return 0.34
    return 0.30

# -------- texte -> phrases (Piper découpe déjà en phrases ; on synthétise phrase par phrase
# pour garder une intonation naturelle, sans couper aux virgules)
def sentences(text):
    text = re.sub(r'((?:\.\.\.|[.,!?:…])+)\*', r'*\1', text)
    parts = re.findall(r'.+?(?:\.\.\.|[.!?…]+)(?=\s|$)|.+$', text)
    return [p.strip() for p in parts if re.search(r"\w", p)]

audio = [np.zeros(int(0.12*SR), np.float32)]
t = 0.12
segs = []

def el_tts(text, prev_text, next_text):
    """ElevenLabs : audio (float, 44.1 kHz) + alignement caractère par caractère. Cache local."""
    import base64, hashlib, urllib.request
    key = hashlib.md5(json.dumps([EL_VOICE, EL_MODEL, text, prev_text, next_text]).encode()).hexdigest()
    os.makedirs(".el_cache", exist_ok=True); cp = f".el_cache/{key}.json"
    if os.path.exists(cp): d = json.load(open(cp))
    else:
        body = {"text": text, "model_id": EL_MODEL, "language_code": "fr", "previous_text": prev_text, "next_text": next_text,
                "voice_settings": {"stability": float(os.environ.get("EL_STABILITY", "0.4")), "similarity_boost": 0.8, "style": float(os.environ.get("EL_STYLE", "0.35")), "use_speaker_boost": True}}
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE}/with-timestamps?output_format=mp3_44100_128",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "xi-api-key": os.environ.get("ELEVEN_API_KEY", "via-proxy")})
        d = json.load(urllib.request.urlopen(req, timeout=120)); json.dump(d, open(cp, "w"))
    tmpd = tempfile.mkdtemp(); open(f"{tmpd}/a.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmpd}/a.mp3", "-ac", "1", "-ar", "44100", f"{tmpd}/a.wav"], check=True)
    with wave.open(f"{tmpd}/a.wav") as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a, d["alignment"]

if ENGINE == "elevenlabs":
    cleans = [sg["text"].replace("*", "") for sg in script["segments"]]
    for i, seg in enumerate(script["segments"]):
        clean = cleans[i]
        a, al = el_tts(clean, " ".join(cleans[max(0, i-2):i]), cleans[i+1] if i+1 < len(cleans) else "")
        # coupe le silence de début, garde l'offset pour les timings
        idx = np.where(np.abs(a) > 0.01)[0]; off = max(0, idx[0] - int(.03*SR)) if len(idx) else 0
        end = min(len(a), idx[-1] + int(.08*SR)) if len(idx) else len(a)
        a = a[off:end]; o = off / SR
        chars, cs, ce = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
        txt = re.sub(r'((?:\.\.\.|[.,!?:…])+)\*', r'*\1', seg["text"])
        words = []; pos = 0
        for tk in txt.split():
            ct = tk.replace("*", "")
            j = clean.find(ct, pos)
            if j < 0: j = pos
            pos = j + len(ct)
            letters = [k for k in range(j, min(pos, len(chars))) if re.match(r"\w", chars[k])] or [min(j, len(chars)-1)]
            words.append({"w": tk, "s": round(t + max(0, cs[letters[0]] - o), 3), "e": round(t + max(0, ce[letters[-1]] - o), 3)})
        s_start = t; audio.append(a); t += len(a) / SR
        p = float(os.environ.get("EL_PAUSE", "0.3")); audio.append(np.zeros(int(p*SR), np.float32)); t += p
        segs.append({"scene": seg["scene"], "start": round(s_start, 3), "end": round(t, 3), "words": words})

for seg in (script["segments"] if ENGINE == "piper" else []):
    s_start = t; words = []
    for sent in sentences(seg["text"]):
        clean = sent.replace("*", "")
        chunks = list(voice.synthesize(clean, syn_config=CFG))
        a = trim(np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32), SR)
        dur = len(a) / SR
        # poids par mot = nb de phonèmes (+ pause pour la ponctuation)
        phon = " ".join("".join(c.phonemes) for c in chunks)
        pwords = [p for p in re.split(r"\s+", phon) if re.search(r"\w", p)]
        toks = sent.split()
        toks_w = [tk for tk in toks if re.search(r"\w", tk)]
        if len(pwords) == len(toks_w):
            it = iter(len(re.sub(r"[ˈˌ̃]", "", p)) for p in pwords)
            weights = [next(it) + 1 if re.search(r"\w", tk) else 0 for tk in toks]
        else:
            weights = [len(re.sub(r"\W", "", tk)) + 1 for tk in toks]
        # une virgule = petite pause après le mot
        weights = [w + (4 if re.search(r"[,:;]\*?$", tk) else 0) + (6 if tk.rstrip("*").endswith("...") and tk != toks[-1] else 0) for w, tk in zip(weights, toks)]
        tot = sum(weights) or 1; acc = 0
        for w, wt in zip(toks, weights):
            words.append({"w": w, "s": round(t + dur*acc/tot, 3), "e": round(t + dur*(acc+wt)/tot, 3)})
            acc += wt
        audio.append(a); t += dur
        p = end_pause(sent); audio.append(np.zeros(int(p*SR), np.float32)); t += p
    segs.append({"scene": seg["scene"], "start": round(s_start, 3), "end": round(t, 3), "words": words})

for s in segs:   # surlignage *mot* (éventuellement sur plusieurs mots)
    inside = False
    for w in s["words"]:
        raw = w["w"]; st = raw.startswith("*"); en = raw.rstrip(".,!?:…").endswith("*")
        w["hl"] = inside or st
        if st and not en: inside = True
        if en: inside = False
        w["w"] = raw.replace("*", "")

# -------- mastering voix (ffmpeg) : passe-haut, chaleur, présence, compression, légère pièce
raw = np.concatenate(audio)
tmp = tempfile.mkdtemp()
def wwrite(p, a, sr):
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(a, -1, 1)*32767).astype(np.int16).tobytes())
wwrite(f"{tmp}/v.wav", raw, SR)
MASTER = os.environ.get("MASTER", "0") == "1"   # traitement voix désactivé par défaut (voix 1 brute, validée)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/v.wav", "-af",
    "aresample=44100:resampler=soxr,alimiter=limit=0.95" if not MASTER else "aresample=44100:resampler=soxr,highpass=f=75,equalizer=f=160:t=q:w=1.2:g=3,equalizer=f=3200:t=q:w=1.5:g=2.5,"
    "equalizer=f=7500:t=q:w=2:g=-2,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,"
    "aecho=0.8:0.6:28|47:0.10|0.06,alimiter=limit=0.95", "-ar", str(SR_OUT), f"{tmp}/vm.wav"], check=True)
with wave.open(f"{tmp}/vm.wav") as w:
    voice_track = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
total = len(voice_track) / SR_OUT + 1.0

# -------- musique de fond
mus = script.get("music", {}) or {}
# volume de la musique : très bas par défaut (l'utilisateur la trouvait trop forte). "music": false => pas de musique
MUSIC_VOL = 0.0 if script.get("music") is False else float(os.environ.get("MUSIC_VOL", mus.get("volume", 0.0)))
def pluck(freq, dur, decay=0.996):
    n = int(SR_OUT*dur); p = int(SR_OUT/freq); buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = decay*0.5*(buf[i % p]+buf[(i+1) % p])
    return out
note = lambda m: 440*2**((m-69)/12)
bpm = mus.get("bpm", 112); step = 60/bpm/2
prog = mus.get("prog", [[60,64,67,72],[57,60,64,69],[53,57,60,65],[55,59,62,67]])
music = np.zeros(int(total*SR_OUT)+SR_OUT); cache = {}
def add(buf, sig, t0, g):
    i = int(t0*SR_OUT); j = min(len(buf), i+len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[:j-i]*g
pattern = [0,2,1,3,2,1,3,2]
for k in (range(int(total/step)+1) if MUSIC_VOL > 0 else []):
    chord = prog[(k//8) % len(prog)]; t0 = k*step; m = chord[pattern[k % 8]] + mus.get("transpose", 12)
    if m not in cache: cache[m] = pluck(note(m), .5)
    add(music, cache[m], t0, .22 if k % 2 == 0 else .15)
    if k % 4 == 0:
        b = chord[0]-24
        if ("b", b) not in cache: cache[("b", b)] = pluck(note(b), .9, .998)
        add(music, cache[("b", b)], t0, .35)
music = music[:int(total*SR_OUT)]; music /= np.abs(music).max()+1e-9 if MUSIC_VOL > 0 else 1
# adoucit la musique (passe-bas) pour qu'elle reste en fond
if MUSIC_VOL > 0:
    _k = np.exp(-2*np.pi*1800/SR_OUT); _y = np.zeros_like(music); _acc = 0.0
    for _i in range(len(music)): _acc = (1-_k)*music[_i] + _k*_acc; _y[_i] = _acc
    music = _y / (np.abs(_y).max()+1e-9)

# -------- bruitages (bibliothèque lib/sfx.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sfx as SFXLIB
def flush(d=1.4):
    n = int(d*SR_OUT); tt = np.arange(n)/SR_OUT; x = rng.normal(0, 1, n); y = np.zeros(n); acc = 0
    for i in range(n): acc += .08*(x[i]-acc); y[i] = acc
    gurgle = 1 + .6*np.sin(2*np.pi*(9 + 6*tt)*tt)
    return y*gurgle*np.minimum(1, tt*12)*np.exp(-tt*1.6)*6
SFX = dict(SFXLIB.SFX); SFX["flush"] = flush
fx = np.zeros_like(music); amb = np.zeros_like(music)
prev = None
for s in segs:   # petit whoosh discret aux changements de scène
    if prev is not None and s["scene"] != prev: add(fx, SFX["whoosh"](), s["start"]-.18, .25)
    prev = s["scene"]
def norm_word(x): return re.sub(r"\W", "", x.lower())
for rule in script.get("sfx", []):
    kind = rule["type"]; dur = rule.get("dur")
    sig = SFX[kind](dur) if dur else SFX[kind]()
    times = []
    if "scene" in rule:
        st = [s["start"] for s in segs if s["scene"] == rule["scene"]]
        if st: times = [st[0] + rule.get("at", 0)]
    else:
        k = 0
        for s in segs:
            if rule.get("in") and s["scene"] != rule["in"]: continue
            for w in s["words"]:
                if norm_word(w["w"]).startswith(norm_word(rule["word"])):
                    if rule.get("n") is None or rule["n"] == k: times.append(w["s"])
                    k += 1
    target = amb if rule.get("ambient", kind in SFXLIB.LONG) else fx
    for t0 in times:
        for r in range(rule.get("repeat", 1)):
            add(target, sig, t0 + rule.get("offset", 0) + r*rule.get("gap", .3), rule.get("gain", .7))

vt = np.zeros_like(music); vt[:len(voice_track)] = voice_track[:len(vt)]
env = np.convolve(np.abs(vt), np.ones(4410)/4410, mode="same")
duck = 1-.6*np.clip(env*12, 0, 1)
mix = vt + music*MUSIC_VOL*duck + fx*.45 + amb*.3*(1-.45*np.clip(env*12, 0, 1))
mix /= max(1.0, np.abs(mix).max()/.97)
wwrite("audio_mix.wav", mix, SR_OUT); wwrite("voice_only.wav", vt, SR_OUT)
json.dump({"duration": round(total, 3), "segments": segs}, open("timings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("voix: %s | durée totale: %.1fs" % (VOICE if ENGINE == "piper" else "ElevenLabs " + EL_VOICE, total))
