"""Check KLAVA's canonical Markdown paths without network access.

This audit does not write to GitHub, Google Drive, Slack, or ChatGPT.
Run from the repository root with: python scripts/check_resource_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:")


def find_broken_local_links(file: Path) -> list[str]:
    """List local Markdown targets missing relative to the given file."""
    errors = []
    for target in MARKDOWN_LINK.findall(file.read_text(encoding="utf-8")):
        path = target.strip().split()[0].strip("<>")
        if not path or path.startswith(("#", "//")):
            continue
        if path.lower().startswith(SKIP_SCHEMES):
            continue
        decoded = unquote(urlsplit(path).path)
        if decoded and not (file.parent / decoded).exists():
            errors.append(f"{file}: missing local link {target}")
    return errors


def main() -> int:
    """Validate tracked top-level governance/docs references; never mutate files."""
    root = Path(__file__).resolve().parents[1]
    files = [root / "README.md", root / "CONSTITUTION.md"]
    files += sorted((root / "docs").glob("*.md"))
    required = [
        root / "CONSTITUTION.md",
        root / "docs" / "RESOURCE-REGISTRY.md",
        root / "docs" / "PROJECT-SPECIFICATION.md",
        root / "docs" / "DEVELOPMENT.md",
        root / "docs" / "CHATGPT-PROJECT-INSTRUCTIONS.md",
    ]
    errors = [f"missing required file: {path}" for path in required if not path.exists()]
    for path in files:
        if path.exists():
            errors.extend(find_broken_local_links(path))
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"Resource audit FAILED: {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print(f"Resource audit passed: {len(files)} Markdown files; local targets exist.")
    print("External Drive, Slack, ChatGPT and HTTP links were NOT checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
