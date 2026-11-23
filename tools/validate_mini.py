"""Validates tools/mini_campaign.json: per-face geometry, numbering, clue<->answer alignment, wordplay correctness,
plus campaign-wide rules (no repeated answers, varied black-square layouts)."""
import json, re, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
camp = json.loads((root/"tools/mini_campaign.json").read_text(encoding="utf-8"))
errs, warns, layouts, total = [], [], {}, 0
seen_ans = {}; all_seen = {}
norm = lambda s: re.sub(r"[^A-Z]", "", s.upper())

def check_face(face):
    N, G, fid = face["size"], face["grid"], face["id"]
    if len(G) != N or any(len(r) != N for r in G): errs.append(f"{fid}: grid is not {N}x{N}"); return
    blk = lambda r, c: r < 0 or c < 0 or r >= N or c >= N or G[r][c] == "#"
    if any((G[r][c] == "#") != (G[N-1-r][N-1-c] == "#") for r in range(N) for c in range(N)): errs.append(f"{fid}: black squares not rotationally symmetric")
    slots, k = {}, 0
    for r in range(N):
        for c in range(N):
            if blk(r, c): continue
            a = blk(r, c-1) and not blk(r, c+1); d = blk(r-1, c) and not blk(r+1, c)
            if a or d: k += 1
            if blk(r, c-1) and blk(r, c+1) or blk(r-1, c) and blk(r+1, c): errs.append(f"{fid}: cell {r},{c} is unchecked")
            for dd, st in (("A", a), ("D", d)):
                if st:
                    w, x, y = "", r, c
                    while not blk(x, y): w += G[x][y]; x, y = (x, y+1) if dd == "A" else (x+1, y)
                    slots[(dd, k)] = w
    for key, w in slots.items():
        if len(w) < 3: errs.append(f"{fid} {key}: word shorter than 3 letters")
        if w in seen_ans: errs.append(f"{fid} {key}: answer {w} already used in {seen_ans[w]}")
        seen_ans.setdefault(w, fid)
    seen = set()
    for c in face["clues"]:
        key = (c["d"], c["n"]); seen.add(key); q, w = c["q"], c["w"]; t = w["t"]
        if key not in slots: errs.append(f"{fid} {key}: clue for a slot that does not exist"); continue
        ans = slots[key]; tag = f"{fid} {key[1]}{key[0]} {ans}"
        m = re.search(r"\((\d+)\)\s*$", q)
        if not m or int(m.group(1)) != len(ans): errs.append(f"{tag}: enumeration missing or wrong")
        if re.search(r"\b%s\b" % ans, q, re.I): errs.append(f"{tag}: clue contains its own answer")
        if t == "anagram" and not (sorted(norm(w["fodder"])) == sorted(ans) and norm(w["fodder"]) != ans): errs.append(f"{tag}: anagram fodder {w['fodder']} does not rearrange to answer")
        elif t == "hidden" and ans not in norm(w["text"]): errs.append(f"{tag}: not hidden in {w['text']!r}")
        elif t == "hidden" and w["text"].lower() not in q.lower(): errs.append(f"{tag}: hidden text {w['text']!r} not shown in clue")
        elif t == "charade" and "".join(p[0] for p in w["parts"]) != ans: errs.append(f"{tag}: charade parts do not spell the answer")
        elif t == "deletion":
            s, x = w["src"], w["removed"]
            if not any(s[:i]+s[i+len(x):] == ans and s[i:i+len(x)] == x for i in range(len(s))): errs.append(f"{tag}: deleting {x} from {s} does not give answer")
            if s.lower() not in q.lower(): errs.append(f"{tag}: source word {s} not in clue")
        elif t == "reversal" and w["src"][::-1] != ans: errs.append(f"{tag}: reversal of {w['src']} is not the answer")
        elif t not in ("anagram", "hidden", "charade", "deletion", "reversal", "double"): errs.append(f"{tag}: unknown wordplay type {t}")
        if t in ("anagram", "hidden", "deletion", "reversal") and w.get("ind", "").lower() not in q.lower(): errs.append(f"{tag}: indicator {w.get('ind')!r} not in clue text")
        if t == "anagram" and w["fodder"].lower() not in q.lower(): errs.append(f"{tag}: fodder {w['fodder']} not in clue")
    for key in slots:
        if key not in seen: errs.append(f"{fid} {key} {slots[key]}: no clue")
    lay = tuple("".join("#" if x == "#" else "." for x in r) for r in G)
    if lay in layouts: warns.append(f"{fid}: same black-square layout as {layouts[lay]}")
    layouts.setdefault(lay, fid)
    return len(slots)

for cu in camp["cubes"]:
    seen_ans = {}; layouts = {}
    if len(cu["faces"]) != 6: errs.append(f"{cu['id']}: a cube needs exactly 6 faces")
    for f in cu["faces"]: total += check_face(f) or 0
    for w, fid in seen_ans.items():
        if w in all_seen: warns.append(f"{cu['id']}: {w} also appears in {all_seen[w]}")
        all_seen.setdefault(w, cu["id"])
print("\n".join(["ERROR " + e for e in errs] + ["warning " + w for w in warns]) or f"Campaign OK: {len(camp['cubes'])} cubes, {total} words, unique within each cube")
if not errs and warns: print(f"Campaign OK with {len(warns)} warning(s)")
sys.exit(1 if errs else 0)
