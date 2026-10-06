#!/usr/bin/env python3
"""Regenerate assets/header.svg from live GitHub language data.

The profile header is generated, not hand-drawn. This script sums the language
bytes GitHub reports for each public, non-fork repo, turns the top languages
into a donut, and writes the SVG.

Run it by hand:

    python scripts/generate_hero.py

Or let .github/workflows/refresh-hero.yml run it on a schedule. Set GITHUB_TOKEN
to raise the API rate limit (the workflow does this for you). If the API is
unreachable the script leaves the existing SVG untouched and exits cleanly, so
a transient failure never produces a broken header.
"""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

USER = "Moustafa-Ahmed"
OUT = Path(__file__).resolve().parent.parent / "assets" / "header.svg"
TOP_N = 5
OTHER_LABEL = "Other"
OTHER_COLOR = "#64748b"

# Cycled in order; tuned to sit next to the header's dark navy background.
PALETTE = ["#38bdf8", "#f472b6", "#fbbf24", "#a78bfa", "#34d399", "#22d3ee"]

# Donut geometry and identity block. Kept here so the layout is reproducible.
CX, CY, RO, RI = 1100.0, 160.0, 82.0, 54.0
WIDTH, HEIGHT = 1280, 340

API = "https://api.github.com"


def api_get(path: str, token: str | None) -> object:
    url = path if path.startswith("http") else API + path
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USER}-profile-hero",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_language_bytes(token: str | None) -> dict[str, int]:
    """Sum language bytes across the user's public, non-fork repositories."""
    repos: list[dict] = []
    page = 1
    while True:
        batch = api_get(f"/users/{USER}/repos?per_page=100&type=owner&page={page}", token)
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    totals: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork") or repo.get("name") == USER:
            continue
        languages = api_get(f"/repos/{USER}/{repo['name']}/languages", token)
        if not isinstance(languages, dict):
            continue
        for language, byte_count in languages.items():
            totals[language] = totals.get(language, 0) + int(byte_count)
    return totals


def build_slices(totals: dict[str, int]) -> list[tuple[str, float, str]]:
    total = sum(totals.values())
    if total <= 0:
        raise ValueError("no language data")

    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    top = ranked[:TOP_N]
    remainder = sum(bytes_ for _, bytes_ in ranked[TOP_N:])

    slices = [
        (name, bytes_ / total * 100.0, PALETTE[i % len(PALETTE)])
        for i, (name, bytes_) in enumerate(top)
    ]
    # Fold the long tail into one honest slice instead of silently dropping it.
    if remainder / total * 100.0 >= 0.1:
        slices.append((OTHER_LABEL, remainder / total * 100.0, OTHER_COLOR))
    return slices


def _pt(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def _slice_path(cx: float, cy: float, ro: float, ri: float, a0: float, a1: float) -> str:
    large = 1 if (a1 - a0) > 180 else 0
    x0, y0 = _pt(cx, cy, ro, a0)
    x1, y1 = _pt(cx, cy, ro, a1)
    x2, y2 = _pt(cx, cy, ri, a1)
    x3, y3 = _pt(cx, cy, ri, a0)
    return (
        f"M{x0:.2f} {y0:.2f} "
        f"A{ro} {ro} 0 {large} 1 {x1:.2f} {y1:.2f} "
        f"L{x2:.2f} {y2:.2f} "
        f"A{ri} {ri} 0 {large} 0 {x3:.2f} {y3:.2f} Z"
    )


def build_svg(slices: list[tuple[str, float, str]]) -> str:
    paths, angle = [], -90.0
    for _, pct, color in slices:
        sweep = 360.0 * pct / 100.0
        paths.append(
            f'    <path d="{_slice_path(CX, CY, RO, RI, angle, angle + sweep)}" '
            f'fill="{color}" stroke="#0b1220" stroke-width="2.5"/>'
        )
        angle += sweep
    slice_svg = "\n".join(paths)

    step = 32.0
    y = CY - (len(slices) - 1) * step / 2.0
    rows = []
    for name, pct, color in slices:
        rows.append(
            f'      <circle cx="792" cy="{y:.0f}" r="6" fill="{color}"/>'
            f'<text x="810" y="{y + 5:.0f}" fill="#94a3b8">{name}</text>'
            f'<text x="985" y="{y + 5:.0f}" fill="#e2e8f0" text-anchor="end" '
            f'font-weight="600">{pct:.2f}%</text>'
        )
        y += step
    legend_svg = "\n".join(rows)

    top_name, top_pct, _ = slices[0]
    summary = ", ".join(f"{name} {pct:.2f}%" for name, pct, _ in slices)
    aria = f"Moustafa Ahmed, backend engineer. Most used languages: {summary}."

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{aria}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#070b16"/>
      <stop offset="0.6" stop-color="#0b1220"/>
      <stop offset="1" stop-color="#0c1526"/>
    </linearGradient>

    <radialGradient id="glowA" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0.26"/>
      <stop offset="1" stop-color="#22d3ee" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#818cf8" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#818cf8" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="nameFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#f8fafc"/>
      <stop offset="0.42" stop-color="#f8fafc"/>
      <stop offset="0.5" stop-color="#22d3ee"/>
      <stop offset="0.58" stop-color="#a78bfa"/>
      <stop offset="0.66" stop-color="#f8fafc"/>
      <stop offset="1" stop-color="#f8fafc"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-0.7 0; 0.7 0; -0.7 0" dur="9s" repeatCount="indefinite"/>
    </linearGradient>

    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.3" fill="#334155" fill-opacity="0.45"/>
    </pattern>
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}" rx="20" fill="url(#bg)"/>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="20" fill="url(#dots)"/>
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="19.5" fill="none" stroke="#1c2536"/>

  <circle cx="140" cy="20" r="300" fill="url(#glowA)"/>
  <circle cx="1190" cy="340" r="330" fill="url(#glowB)"/>

  <!-- identity -->
  <text x="74" y="150" fill="#22d3ee" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="18" font-weight="600" letter-spacing="7">BACKEND ENGINEER</text>
  <text x="72" y="244" fill="url(#nameFill)" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="82" font-weight="800" letter-spacing="-1.5">Moustafa Ahmed</text>

  <!-- languages donut -->
  <g>
{slice_svg}
    <text x="{CX:.0f}" y="{CY - 4:.0f}" fill="#e2e8f0" text-anchor="middle"
          font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="22" font-weight="700">{top_name}</text>
    <text x="{CX:.0f}" y="{CY + 18:.0f}" fill="#7c8aa0" text-anchor="middle"
          font-family="Menlo, Consolas, monospace" font-size="13">{top_pct:.1f}%</text>
  </g>

  <g font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="15">
{legend_svg}
  </g>

  <!-- data bus -->
  <line x1="72" y1="326" x2="1240" y2="326" stroke="#16203a" stroke-width="2"/>
  <line x1="72" y1="326" x2="1240" y2="326" stroke="#22d3ee" stroke-width="2" stroke-linecap="round"
        stroke-dasharray="60 1108" opacity="0.75">
    <animate attributeName="stroke-dashoffset" from="1168" to="-60" dur="7s" repeatCount="indefinite"/>
  </line>
  <g fill="#243049">
    <circle cx="200" cy="326" r="3.5"/>
    <circle cx="392" cy="326" r="3.5"/>
    <circle cx="584" cy="326" r="3.5"/>
    <circle cx="968" cy="326" r="3.5"/>
    <circle cx="1160" cy="326" r="3.5"/>
  </g>
</svg>
'''


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    try:
        totals = fetch_language_bytes(token)
        slices = build_slices(totals)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError) as exc:
        print(f"hero: skipping refresh ({exc})", file=sys.stderr)
        return 0

    for name, pct, _ in slices:
        print(f"  {name:<12} {pct:5.2f}%")

    svg = build_svg(slices)
    if OUT.exists() and OUT.read_text() == svg:
        print("hero: no change")
        return 0
    OUT.write_text(svg)
    print(f"hero: wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
