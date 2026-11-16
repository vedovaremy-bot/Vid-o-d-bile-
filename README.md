# Vidéos débiles — format court animé (> 60 s)

## Vidéo 01 — « Le pigeon qui t'a fait un procès » (71 s, 1080x1920)
Fichier final : `video01_pigeon_proces.mp4`

### Régénérer / créer une nouvelle vidéo
1. Écrire l'histoire dans `video01/script.json` (les `*mots*` entre astérisques s'affichent en jaune).
2. Voix off (Piper, voix FR masculine `fr_FR-tom-medium`, à placer dans `video01/voice/`) + musique + bruitages :
   `python3 tts.py`  -> `audio_mix.wav`, `timings.json`
3. Animation + sous-titres mot par mot (`scene.html`, rendu via Playwright) :
   `node render.js` -> `out/video.mp4`  (`node render.js 5 12` = images de test)

## Vidéo 02 — « L'escargot qui te poursuit depuis 7 ans » (80 s)
Fichier final : `video02_escargot_7ans.mp4` — voix `fr_FR-miro-high` (test). **Voix retenue pour la suite : `fr_FR-tom-medium` (voix 1).**

Moteur commun dans `lib/` (`engine.js`, `tts.py`, `render.js`). Nouvelle vidéo :
```
mkdir videoXX && cd videoXX   # script.json + scene.html (voir video02)
python3 ../lib/tts.py         # VOICE=fr_FR-upmc-medium SPEAKER=1 pour changer de voix
node ../lib/render.js
```
Les modèles de voix (`voices/`) se téléchargent depuis
`https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-<voix>.tar.bz2`.
