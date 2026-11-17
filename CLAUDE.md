# Consignes du projet (vidéos débiles monétisables)

- **Voix off : ElevenLabs, voix `3Tp5mYhT9wrfnry9pzvV`** (modèle `eleven_multilingual_v2`), validée par l'utilisateur
  pour toutes les vidéos. C'est le défaut de `lib/tts.py`. Nécessite l'environnement cloud « video-faceless »
  (clé API injectée par le proxy pour api.elevenlabs.io). Cette voix parle vite : viser ~200 mots pour dépasser 65 s.
  Secours uniquement si ElevenLabs est inaccessible : `ENGINE=piper` (ancienne voix 1 `fr_FR-tom-medium`), et le dire à l'utilisateur.
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
