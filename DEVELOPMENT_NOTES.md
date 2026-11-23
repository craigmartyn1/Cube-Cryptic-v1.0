# Development notes

## Status
- `index.html` is generated: edit `tools/mini_campaign.json` (puzzle data) or `tools/mini.template.html` (engine/UI), then run `python tools/build_mini.py` and `python tools/validate_mini.py`. CI fails if `index.html` is out of date.
- The old solid-cube game (3x3/4x4 packs) was retired and removed; it remains in git history.
- No manifest/service worker exists yet: do not claim offline/PWA support until implemented and tested.
- No Android APK/AAB is included. Automated tests ran in a simulated browser only; real-device testing is still outstanding.

## Ladder rules (index.html, see CFG in tools/mini.template.html)
- Cube grade by hints per face: mastered <=1.0, solid <=1.5, heavy >=2.5, otherwise cleared.
- A size stage promotes when every cube in it is done and the average is <=1.5 hints per face.
- Two heavy cubes in a row above the smallest size caps the player at the next size down until a non-heavy cube is cleared there.
- Hint tokens: start 5, max 9, +1 per hint-free face, +2 mastered cube, +1 solid cube, +1 per new day. Hints cost 1 token.
- Save key `cubeLadder_v1` (includes a content fingerprint; changed puzzle data resets progress). Edit puzzle data in `tools/mini_campaign.json`, then run `python tools/build_mini.py` and `python tools/validate_mini.py`.
- Stage length: the first `CFG.cubesPerStage` (now 2) cubes of a size must be cleared, averaging <=1.5 hints per face, to open the next size. Extra cubes of that size stay available as optional practice.
