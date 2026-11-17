# Consignes du projet (vidéos débiles monétisables)

- **Voix off : ElevenLabs, voix `3Tp5mYhT9wrfnry9pzvV`** (modèle `eleven_multilingual_v2`), validée par l'utilisateur
  pour toutes les vidéos. C'est le défaut de `lib/tts.py`. Nécessite l'environnement cloud « video-faceless »
  (clé API injectée par le proxy pour api.elevenlabs.io). Cette voix parle vite : viser ~200 mots pour dépasser 65 s.
  Secours uniquement si ElevenLabs est inaccessible : `ENGINE=piper` (ancienne voix 1 `fr_FR-tom-medium`), et le dire à l'utilisateur.
- Format : vertical 1080x1920, **plus de 60 s**, histoire VRAIMENT débile et absurde (nonsense, jeux de mots idiots, personnages objets/animaux qui parlent — comme le pigeon ou le caca ; éviter les histoires trop logiques) racontée à la 2e personne (« tu »),
  hook très fort dans la 1re phrase, sous-titres mot par mot (blanc + mots-clés jaunes), style dessin animé 2D.
- Pipeline : `videoXX/script.json` + `videoXX/scene.html` → `python3 ../lib/tts.py` → `node ../lib/render.js`.
- Demande de like par le personnage principal vers 10 s (fait sur la vidéo 10) : pas encore confirmé pour toutes les vidéos, demander à l'utilisateur.
