# Cube Cryptic development roadmap

## Stage 1 — Crossword engine and reliability
- [x] Six-face interactive cube and crossword clues
- [x] Four campaign packs, including the four-letter wordplay pack
- [x] Defensive save/load and scoring safeguards
- [ ] Expand and validate 5x5 and 6x6 layouts (cube grid size is data-driven; needs a word-square generator/validator and larger face sizing)
- [ ] Editorial review of clue quality and explanations
- [ ] Full browser and Android device QA

## Stage 1b — Black-square crosswords (replaces solid cubes)
- [x] 5x5 engine + validator proven on one face (`mini.html`)
- [x] Cube 1 and Cube 2 (5x5, six faces each) authored with structured clues
- [ ] Cubes 3-5 at 5x5
- [x] Black-square faces wired into the game with stars, saves and finale
- [x] Ladder: hint tokens, mastery grades, promotion to the next size, drop-back after two heavy-hint cubes
- [x] 3D cube face selector, rank-coloured themes, how-to-play guide
- [x] Legacy solid-cube game removed (kept in git history)
- [ ] 6x6 to 9x9 stages (engine ready; solver proven on sparse layouts; blocked on a curated common-word list so fills avoid names/obscure words, then ~12 clues per face to author; see tools/fill_grid.py)
- [ ] Original line: 6x6 to 9x9 stages (target 15x15 later; needs pinch-zoom grid and a larger validated clue bank)

## Stage 2 — Campaign progression and rewards
- [x] Campaign unlock rules (finish a campaign to unlock the next; `?unlockall` URL flag for testing)
- [ ] Progression map
- [x] Completion screen: stars, best score, time, Next campaign button, cube celebration
- [ ] Face-level rewards
- [ ] Unlockable cube themes and persistence
- [ ] Regression tests for existing saves and scoring

## Stage 3 — Cryptic clue depth
- [ ] Broader cryptic clue mechanisms
- [ ] Clear, accurate clue explanations
- [ ] Editorial QA and difficulty balancing

## Stage 4 — Engagement and polish
- [ ] Daily puzzles
- [ ] Achievements and progression feedback
- [ ] Animations, accessibility and settings polish

## Stage 5 — Android release
- [ ] Offline install/package strategy
- [ ] Android APK/AAB build pipeline
- [ ] Device and performance testing
- [ ] Privacy policy, store listing and Google Play release checks

## Release gate
A milestone is complete only after its source changes are committed, validation passes, and a downloadable build is produced and checked.

## Findings on generating bigger grids (for whoever continues)
- 5x5 faces with black squares fill well from a ~15k-word list (wordfreq + a dictionary, names removed).
- 6x6 does not: dense layouts have no fills from common words; sparse layouts fill, but lean on 3-letter abbreviations and obscure words. A 5.5k curated list (google-20k + dictionary + NLTK names removed) was too small even for 5x5.
- Needed next: a larger curated *clean* word list with part-of-speech/definitions (so clues can be drafted from definitions, not just wordplay), a stronger solver (word-list tries, restarts), and a human curation pass per grid.
- Pinch-zoom/scroll grid is required for 10x10 and above; 15x15 means about 70 clues per face, so it needs a clue bank, not hand authoring.
