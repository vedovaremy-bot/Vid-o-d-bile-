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
Fichier final : `video02_escargot_7ans.mp4` — **Voix retenue pour la suite : `fr_FR-tom-medium` (voix 1).**

Moteur commun dans `lib/` (`engine.js`, `tts.py`, `render.js`). Nouvelle vidéo :
```
mkdir videoXX && cd videoXX   # script.json + scene.html (voir video02)
python3 ../lib/tts.py         # VOICE=fr_FR-upmc-medium SPEAKER=1 pour changer de voix
node ../lib/render.js
```
Les modèles de voix (`voices/`) se téléchargent depuis
`https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-<voix>.tar.bz2`.

## Vidéo 03 — « Ton caca a refusé de partir » (70 s)
Fichier final : `video03_caca_president.mp4` — voix 1 (`fr_FR-tom-medium`).

## Vidéo 04 — « Ton chat a vendu ta maison » (70 s)
Fichier final : `video04_chat_maison.mp4` — voix 1 (`fr_FR-tom-medium`).

## Vidéo 05 — « Ta mamie a mis K.O. un champion de MMA » (70 s)
Fichier final : `video05_mamie_mma.mp4` — voix 1 (`fr_FR-tom-medium`).

## Vidéo 06 — « Tu as répondu "toi aussi" au serveur » (69 s)
Fichier final : `video06_toi_aussi.mp4` — voix 1. Pensée pour la viralité : situation vécue par tout le monde,
callback de la blague au mariage, question en commentaire à la fin.

## Vidéo 07 — « Tu as liké une photo de ton ex de 2017 » (70 s)
Fichier final : `video07_like_ex.mp4` — voix 1. Appel à l'action : identifier quelqu'un en commentaire.

## Vidéo 08 — « Tu as refusé de faire demi-tour » (70 s)
Fichier final : `video08_gps_vexe.mp4` — voix 1.

## Vidéo 09 — « Ton nez s'est barré » (70 s)
Fichier final : `video09_nez_barre.mp4` — voix 1. Retour à l'absurde pur (demande de l'utilisateur :
les vidéos doivent être *vraiment* débiles, comme le pigeon et le caca — pas de "relatable" trop logique).

## Vidéo 10 — « Une saucisse a pris ta place au travail » (70 s)
Fichier final : `video10_saucisse_bureau.mp4` — voix 1. Vers 10-13 s, le personnage principal (la saucisse)
regarde la caméra et réclame un like (« Lâche un like… sinon je prends aussi ta place à la maison »).
Version ElevenLabs (voix `3Tp5mYhT9wrfnry9pzvV`, 68 s) : `video10_saucisse_bureau_elevenlabs.mp4`.

## Vidéo 11 — « Ton réveil ne s'arrête plus » (74 s)
Fichier final : `video11_reveil.mp4` — voix ElevenLabs, sans musique, ~30 bruitages synchronisés (`lib/sfx.py`),
like réclamé par le réveil vers 25 s.

## Vidéo 12 — « Ta baignoire est partie en vacances » (70 s)
Fichier final : `video12_baignoire_vacances.mp4` — voix ElevenLabs, sans musique, ~40 bruitages, pas de demande de like (alternance).

## Vidéo 13 — « Le like de 2017 est vivant » (partie 2 de la vidéo 07, 68 s)
Fichier final : `video13_like_ex_partie2.mp4` — suite de la vidéo qui a le mieux marché. Voix ElevenLabs, sans musique,
bruitages, like réclamé par le like lui-même vers 35 s.

## Vidéo 14 — « L'armée des chaussettes perdues » (76 s)
Fichier final : `video14_armee_chaussettes.mp4` — voix ElevenLabs, sans musique, ~35 bruitages (dont nouveaux : buzz, clank, washer, shrink), pas de demande de like.

## Vidéo 15 — « Un chevalier est sorti du micro-ondes » (69 s)
Fichier final : `video15_chevalier_micro_ondes.mp4` — voix ElevenLabs, sans musique, ~40 bruitages,
like réclamé par Sire Gontran juste avant la chute (~37-46 s).

## Vidéo 16 — « Ton nouveau coloc est un pingouin » (72 s)
Fichier final : `video16_pingouin_coloc.mp4` — voix ElevenLabs, sans musique, ~37 bruitages, pas de demande de like.

## Vidéo 17 — « Ta brosse à dents a démissionné » (70 s)
Fichier final : `video17_brosse_a_dents.mp4` — voix ElevenLabs, sans musique, ~35 bruitages,
like réclamé par la brosse à dents dès le début (~3-9 s, « c'est mon indemnité de départ »).

## Retour à la voix 1 (Piper `fr_FR-tom-medium`) à partir de la vidéo 18
## Vidéo 18 — « Un hamster a piraté ta carte bancaire » (81 s) — `video18_hamster_carte_bancaire.mp4`, pas de like
## Vidéo 19 — « Ton canapé t'a avalé » (77 s) — `video19_canape_royaume.mp4`, like réclamé par le roi juste avant la fin
## Vidéo 20 — « Un nuage te suit partout » (76 s) — `video20_nuage.mp4`, pas de like
Helpers de scène partagés : `lib/common.js`. Nouveaux bruitages : squeak, thunder, slurp.
## Vidéo 21 — « Ton grille-pain est devenu rappeur » (70 s) — `video21_grille_pain_rappeur.mp4`, voix 1, like en freestyle (~20-29 s)
## Vidéo 22 — « Une mouette a volé ta vie » (68 s) — `video22_mouette.mp4`, voix 1, pas de like
## Vidéo 23 — « Ton ventilateur a décollé » (72 s) — `video23_ventilateur.mp4`, like vers 28 s (+ gag : il souffle les sous-titres, `window.hideSubs`)
## Vidéo 24 — « Ton ombre a démissionné » (71 s) — `video24_ombre.mp4`, pas de like (silhouette via `ctx` swappable dans engine.js)
## Vidéo 25 — « Ta tortue a gagné le Tour de France » (75 s) — `video25_tortue_tour_de_france.mp4`, like vers 14 s (avec compte à rebours)
## Vidéo 26 — « Ton aspirateur robot a pris le pouvoir » (69 s) — `video26_aspirateur_robot.mp4`, pas de like
## Vidéo 27 — « Une vache t'a volé ton skate » (76 s) — `video27_vache_skate.mp4`, like vers 43 s (après le triple salto)
