#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate quality/coverage.md — per-column fill rates for every public CSV.

Numbers are computed from the files in data/; nothing is hand-written. Run after any
data change:

    python3 scripts/build_coverage.py
    python3 scripts/build_coverage.py --check
"""
import csv
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "quality", "coverage.md")

FILES = [
    ("hotels.public.csv", "Public hotel inventory (4–5 star, Asia)", ("lng", "lat")),
    ("venues.public.csv", "Public China venue directory", ("lng", "lat")),
    ("cases.csv", "Case index (links only)", ()),
    ("sample-80-halls-20261027.csv", "80-hotel hall-level sample", ()),
    ("sample-80-venues-20261027.csv", "80-hotel venue-level sample", ("lng", "lat")),
    ("batch2-exhibition-centres-20261029.csv", "Batch 2 — exhibition centres (Asia)", ()),
    ("batch2-exhibition-halls-20261029.csv", "Batch 2 — exhibition halls", ()),
    ("batch3-sports-arts-retail-popup-racing-20261029.csv", "Batch 3 — sports, arts, retail & pop-up, racing", ()),
    ("whitelist-v2.csv", "Public-layer column whitelist", ()),
]


def pct(n, d):
    return f"{n / d * 100:.1f}%" if d else "—"


def build():
    lines = [
        "# Data coverage",
        "",
        "*Generated from the public CSVs by `scripts/build_coverage.py`. Do not edit by hand — "
        "run the script, or CI will flag the difference.*",
        "",
        "A blank cell means **not published or not captured**, never `0` and never `N/A`. "
        "Coverage is per file, per column.",
        "",
    ]
    summary = []
    for fn, label, coord_cols in FILES:
        path = os.path.join(DATA, fn)
        if not os.path.exists(path):
            raise SystemExit(f"missing data file: {path}")
        with open(path, encoding="utf-8-sig", newline="") as fh:
            r = csv.DictReader(fh)
            cols = r.fieldnames or []
            rows = list(r)
        n = len(rows)
        sha = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
        filled = {c: sum(1 for x in rows if (x.get(c) or "").strip()) for c in cols}
        coord = next(((c, filled[c]) for c in coord_cols if c in cols), None)
        summary.append((fn, n, len(cols), coord, sha))
        lines += [
            f"## `{fn}` — {label}",
            "",
            f"{n} rows · {len(cols)} columns · sha256 `{sha}…`",
            "",
            "| Column | Filled | Coverage |",
            "|---|---:|---:|",
        ]
        for c in cols:
            lines.append(f"| `{c}` | {filled[c]} | {pct(filled[c], n)} |")
        if coord:
            lines += [
                "",
                f"**Coordinates:** `{coord[0]}` present on {coord[1]} of {n} rows "
                f"({pct(coord[1], n)}). Datum is WGS-84; see `docs/coordinates.md`.",
            ]
        else:
            lines += ["", "**Coordinates:** no coordinate column in this file."]
        lines.append("")

    lines += [
        "## Summary",
        "",
        "| File | Rows | Columns | Coordinates | sha256 |",
        "|---|---:|---:|---:|---|",
    ]
    for fn, n, nc, coord, sha in summary:
        lines.append(f"| `{fn}` | {n} | {nc} | {pct(coord[1], n) if coord else '—'} | `{sha}…` |")
    lines += ["", "*EVENTTHING · Hong Kong · venue.eventthing.ai*", ""]
    return "\n".join(lines)


def main(check=False):
    text = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if old == text:
        print("coverage up to date")
        return
    if check:
        print("COVERAGE STALE — run python3 scripts/build_coverage.py")
        sys.exit(1)
    open(OUT, "w", encoding="utf-8").write(text)
    print("coverage written:", OUT)


if __name__ == "__main__":
    main("--check" in sys.argv)
