#!/usr/bin/env python3
"""Lightweight checks for this profile repo.

Run before merging (and in CI):

    python scripts/check_repo.py

Verifies that every SVG under assets/ is well-formed XML and that every local
image referenced from the README actually exists, so the page cannot silently
break. No third-party dependencies.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_SRC = re.compile(r'src="([^"]+)"')
REMOTE = ("http://", "https://", "data:", "#")


def local_refs(text: str) -> list[str]:
    refs = [m.group(1) for m in MD_IMG.finditer(text)]
    refs += [m.group(1) for m in HTML_SRC.finditer(text)]
    return [r.split()[0] for r in refs if not r.startswith(REMOTE)]


def main() -> int:
    problems: list[str] = []

    for svg in sorted((ROOT / "assets").glob("*.svg")):
        try:
            ET.parse(svg)
        except ET.ParseError as exc:
            problems.append(f"{svg.relative_to(ROOT)}: not well-formed XML ({exc})")

    if not README.exists():
        problems.append("README.md is missing")
    else:
        for ref in local_refs(README.read_text()):
            if not (ROOT / ref).exists():
                problems.append(f"README references missing file: {ref}")

    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1

    print("OK: assets are well-formed and README references resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
