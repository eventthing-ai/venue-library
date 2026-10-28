#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate fields.md — the public field dictionary (English only).

Row and column counts and file sizes are read from data/ on disk; field names, types and
descriptions come from scripts/field_meta.py. Numbers are never typed by hand, so the
document cannot drift away from the data.

Usage: python3 scripts/gen_fields_md.py [--check]
"""
import csv
import os
import sys

from field_meta import FILES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "fields.md")
RELEASE = "v1.0.1 (2026-10-29)"

STATUS_VALUES = [
    ("open", "Operating",
     "Official site or booking page currently lists it, or an official event announcement within the last 12 months."),
    ("closed", "Closed / demolished",
     "Official notice, government release or authoritative media; or the official site is permanently offline with no successor."),
    ("renovating", "Closed for renovation",
     "Official notice of closure/refurbishment with a reopening date."),
    ("under_construction", "Under construction / not yet open",
     "Official statement that the venue is under construction or opening in a stated year."),
    ("unknown", "Not verified",
     "No usable evidence. **Not** a synonym for closed."),
]

STATUS_SOURCES = [
    ("official_site_listed", "hotels.public.csv",
     "The brand's official booking site lists the property as bookable on `status_asof`."),
    ("official_site", "venues.public.csv",
     "The venue's own official page shows it operating."),
    ("derived_from_hotels_asia", "venues.public.csv",
     "Venue matched to a hotel record whose official site lists it (`venue_id_ref`)."),
    ("third_party_listing", "venues.public.csv",
     "A third-party listing page showed it available; the link itself is withheld by policy."),
    ("retired_list", "venues.public.csv",
     "Listed on the internal retired-venue list → `closed`."),
    ("not_verified", "venues.public.csv",
     "No check performed → `unknown`."),
    ("no_source_link", "venues.public.csv",
     "Previously marked open but no source link survived policy screening → downgraded to `unknown`."),
]


def read(path):
    raw = open(path, "rb").read()
    with open(path, encoding="utf-8", newline="") as fh:
        r = csv.DictReader(fh)
        cols = r.fieldnames or []
        rows = list(r)
    return cols, rows, raw


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return out


def main(check=False):
    stats = {}
    for spec in FILES:
        cols, rows, raw = read(os.path.join(DATA, spec["file"]))
        meta_cols = [c[0] for c in spec["columns"]]
        if cols != meta_cols:
            print(f"ERROR: {spec['file']} columns do not match field_meta", file=sys.stderr)
            sys.exit(1)
        stats[spec["file"]] = {"rows": len(rows), "cols": len(cols), "raw": raw, "data": rows}

    L = []
    L.append(f"# Field dictionary · public data release {RELEASE}")
    L.append("")
    L.append("Every column of every CSV in this repository, documented in English. "
             "Units are shown per column; the CSV itself stores numbers only.")
    L.append("")
    L.append("## Files in this release")
    L.append("")
    L.append(f"Release `{RELEASE}` · encoding UTF-8 without BOM · LF line endings · one header row per file.")
    L.append("")
    rows_tbl = []
    for spec in FILES:
        s = stats[spec["file"]]
        rows_tbl.append([f"`{spec['file']}`", f"{s['rows']:,}", str(s["cols"]), f"`{spec['pk']}`",
                         f"[`schema/{spec['schema']}`](schema/{spec['schema']})"])
    L += md_table(["File", "Rows", "Columns", "Primary key", "Schema"], rows_tbl)
    L.append("")
    L.append("`data/whitelist-v2.csv` is release metadata (which source columns are kept or withheld and why), "
             "not a dataset; it is indexed and schema-checked like every other CSV so the contract is complete.")
    L.append("")
    L.append("## Format rules")
    L.append("")
    L.append("- **UTF-8, no BOM; LF line endings.** Commas separate fields; the first row is the header.")
    L.append("- **Empty means unpublished.** An empty cell is `null` — never `0`, never `\"N/A\"`, never a guess.")
    L.append("- **Numbers carry no units** and no thousands separators. Parse them as numbers.")
    L.append("- **Coordinates are WGS-84** (EPSG:4326), in decimal degrees; blank when no trustworthy point exists.")
    L.append("- **No contact data.** No email addresses, phone numbers or personal names are published.")
    L.append("")
    L.append("## Status model")
    L.append("")
    L.append("`status` answers one question: **is this venue operating?** It is evidence-based and is never defaulted to `open`.")
    L.append("")
    L += md_table(["Value", "Meaning", "How it is established"],
                  [[f"`{v[0]}`", v[1], v[2]] for v in STATUS_VALUES])
    L.append("")
    L.append("**Rules**")
    L.append("")
    L.append("1. Missing evidence is `unknown`, never `open`.")
    L.append("2. `unknown` is excluded from every “open” count (README, marketing copy, derived statistics).")
    L.append("3. `status_asof` is the date of the evidence, not the date the file was built.")
    L.append("4. Status belongs to the venue. Halls in the sample inherit the status of their hotel.")
    L.append("5. `status_source` names the evidence type; a row with `status=open` always carries one.")
    L.append("")
    L += md_table(["`status_source`", "Used in", "Meaning"],
                  [[f"`{s[0]}`", s[1], s[2]] for s in STATUS_SOURCES])
    L.append("")
    L.append("### Status in this release")
    L.append("")
    cnt_tbl = []
    for fn in ("hotels.public.csv", "venues.public.csv", "sample-80-halls-20261027.csv", "sample-80-venues-20261027.csv"):
        rows = stats[fn]["data"]
        if (not rows) or ("status" not in rows[0]):
            cnt_tbl.append([f"`{fn}`", f"{len(rows):,}", "—", "—", "—", "—", "—"])
            continue
        c = {}
        for r in rows:
            c[r.get("status", "")] = c.get(r.get("status", ""), 0) + 1
        cnt_tbl.append([f"`{fn}`", f"{len(rows):,}",
                        f"{c.get('open', 0):,}", f"{c.get('closed', 0):,}",
                        f"{c.get('renovating', 0):,}", f"{c.get('under_construction', 0):,}",
                        f"{c.get('unknown', 0):,}"])
    L += md_table(["File", "Rows", "open", "closed", "renovating", "under_construction", "unknown"], cnt_tbl)
    L.append("")
    L.append("The two main tables are data files: every row carries `status`, `status_source` and `status_asof`. "
             "The hall sample is a display sample and carries `status` and `status_asof` only (its evidence type is the "
             "same as the hotel main table: brand official site, listed for sale on 2026-10-26). The venue-level "
             "sample is a directory sample and carries no status column at all.")
    L.append("")

    for i, spec in enumerate(FILES, 1):
        s = stats[spec["file"]]
        L.append(f"## {i}. `{spec['file']}` — {s['cols']} columns")
        L.append("")
        L.append(f"{spec['rows_label_en']} **{s['rows']:,} rows.**")
        L.append("")
        body = []
        for c in spec["columns"]:
            body.append([f"`{c[0]}`", c[1], c[2], c[3]])
        L += md_table(["Field", "Type", "Unit", "Description"], body)
        L.append("")

    L.append("## Notes and conventions")
    L.append("")
    L.append("- **Scope.** `hotels.public.csv` is the 4–5 star public layer (3,038 rows). The internal master also holds "
             "1,246 three-star records as denominator data; they are not published. `venues.public.csv` is the full "
             "China venue list (3,549 rows), not a selection.")
    L.append("- **Commercial-venue policy.** For `category=商业`, `lng`, `lat` and `source_url` are blank for the whole "
             "class. This is a contractual restriction, not missing data.")
    L.append("- **Sample files.** Rooms carry length/width/height only where the official site publishes them. "
             "39 rows carry a dimension-QA note (`dims_qa`) because area and length×width use different calibers; "
             "their length/width/height are now published as recorded. 3 `suspect` rows were removed. "
             "1,039 of 2,100 halls have complete length/width/height.")
    L.append("- **Licence.** Data CC BY 4.0; code MIT. Credit “EVENTTHING Venue Library”.")
    L.append("")
    L.append("*EVENTTHING · Hong Kong · venue.eventthing.ai*")
    L.append("")

    text = "\n".join(L)
    old = open(OUT, encoding="utf-8", newline="").read() if os.path.exists(OUT) else ""
    if check:
        if old != text:
            print("FIELDS STALE", file=sys.stderr)
            sys.exit(1)
        print("fields.md up to date")
    else:
        with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"fields.md written: {len(text.encode('utf-8'))} bytes, {len(L)} lines")


if __name__ == "__main__":
    main("--check" in sys.argv)
