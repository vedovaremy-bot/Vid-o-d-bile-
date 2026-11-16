# Vidéos débiles — format court animé (> 60 s)

## Vidéo 01 — « Le pigeon qui t'a fait un procès » (71 s, 1080x1920)
Fichier final : `video01_pigeon_proces.mp4`

### Régénérer / créer une nouvelle vidéo
1. Écrire l'histoire dans `video01/script.json` (les `*mots*` entre astérisques s'affichent en jaune).
2. Voix off (Piper, voix FR masculine `fr_FR-tom-medium`, à placer dans `video01/voice/`) + musique + bruitages :
   `python3 tts.py`  -> `audio_mix.wav`, `timings.json`
3. Animation + sous-titres mot par mot (`scene.html`, rendu via Playwright) :
   `node render.js` -> `out/video.mp4`  (`node render.js 5 12` = images de test)
