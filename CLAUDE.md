# Consignes du projet (vidéos débiles monétisables)

- **Voix off : la voix 1 d'origine = `fr_FR-tom-medium` (Piper)**, défaut de `lib/tts.py` (length_scale 0.86, noise 0.667,
  noise_w 0.8, sans mastering). L'utilisateur est revenu à cette voix à partir de la vidéo 18 car les premières vidéos
  faisaient plus de vues. ElevenLabs (voix `3Tp5mYhT9wrfnry9pzvV`, `"engine": "elevenlabs"`) reste disponible mais
  uniquement si l'utilisateur le redemande. Si `voices/` est vide, télécharger la voix :
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-tom-medium.tar.bz2`
- Format : vertical 1080x1920, **plus de 60 s**, histoire VRAIMENT débile et absurde (nonsense, jeux de mots idiots, personnages objets/animaux qui parlent — comme le pigeon ou le caca ; éviter les histoires trop logiques) racontée à la 2e personne (« tu »),
  hook très fort dans la 1re phrase, sous-titres mot par mot (blanc + mots-clés jaunes), style dessin animé 2D.
- Pipeline : `videoXX/script.json` + `videoXX/scene.html` → `python3 ../lib/tts.py` → `node ../lib/render.js`.
- Demande de like : **pas dans toutes les vidéos** (environ une sur deux, en variant). Quand il y en a une, c'est le
  **personnage principal** qui regarde la caméra et réclame le like à sa façon (« lâche un like », « oublie pas le like »,
  « mets-moi un like »… avec une menace ou une blague débile), à un **moment différent à chaque fois** (début, milieu,
  juste avant la chute…), pas toujours vers 10 s. Exemple : vidéo 10 (la saucisse).
- **Pas de musique de fond** (défaut de `lib/tts.py`, demandé par l'utilisateur). À la place, des **bruitages qui collent
  à l'action** (bibliothèque `lib/sfx.py`) : alarme en fond quand une alarme sonne, bruit de chute quand quelqu'un retombe,
  plouf, sirène, pas, porte, applaudissements, trombone de l'échec… Les déclarer dans `script.json` → `sfx`
  (par mot : `{"word": "...", "type": "land"}`, ou par scène : `{"scene": "...", "at": 0.5, "type": "alarm", "dur": 3}`).
  Mettre des bruitages à chaque action visible.
