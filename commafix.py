import re
from pathlib import Path

ROOT = Path(".")

pattern = re.compile(r",(\S)")

for md_path in ROOT.rglob("*.md"):
    text = md_path.read_text(encoding="utf-8")
    new_text = pattern.sub(r", \1", text)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"Fixed: {md_path}")
