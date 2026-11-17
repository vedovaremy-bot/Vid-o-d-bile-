# Consignes du projet (vidéos débiles monétisables)

- **Voix off : toujours la voix 1 = `fr_FR-tom-medium` (Piper)**, choisie par l'utilisateur.
  C'est la voix par défaut de `lib/tts.py` (length_scale 0.86, noise 0.667, noise_w 0.8, sans mastering).
  Ne pas la changer sauf demande explicite. Si `voices/` est vide, la télécharger :
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-tom-medium.tar.bz2`
- Format : vertical 1080x1920, **plus de 60 s**, histoire VRAIMENT débile et absurde (nonsense, jeux de mots idiots, personnages objets/animaux qui parlent — comme le pigeon ou le caca ; éviter les histoires trop logiques) racontée à la 2e personne (« tu »),
  hook très fort dans la 1re phrase, sous-titres mot par mot (blanc + mots-clés jaunes), style dessin animé 2D.
- Pipeline : `videoXX/script.json` + `videoXX/scene.html` → `python3 ../lib/tts.py` → `node ../lib/render.js`.
