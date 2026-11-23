"""Builds index.html (the game) from tools/mini.template.html + tools/mini_campaign.json (single source of truth for the face data)."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
camp = json.loads((root/"tools/mini_campaign.json").read_text(encoding="utf-8"))
html = (root/"tools/mini.template.html").read_text(encoding="utf-8").replace("/*DATA*/", json.dumps(camp, ensure_ascii=False, separators=(",", ":")))
(root/"index.html").write_text(html, encoding="utf-8")
import hashlib
sw = (root/"tools/sw.template.js").read_text(encoding="utf-8").replace("/*VERSION*/", hashlib.sha256(html.encode("utf-8")).hexdigest()[:10])
(root/"sw.js").write_text(sw, encoding="utf-8")
print("built index.html and sw.js")
