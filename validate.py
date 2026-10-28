#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EVENTTHING Venue Library — public-layer validator.

Checks every CSV in data/ against the public contract:

  * UTF-8 without BOM, LF line endings
  * file is listed in schema/_index.json, with matching rows, columns and SHA-256
  * required columns present; key column unique
  * numeric columns parse (empty allowed); coordinates are paired and in range
  * status vocabulary and status_asof date format
  * no personal email address or Chinese mobile number in any cell

Usage:
    python3 validate.py            # validate every file in data/
    python3 validate.py FILE...    # validate selected files
"""
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
INDEX = os.path.join(ROOT, "schema", "_index.json")

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")
PHONE = re.compile(r"(?<![\d.])1[3-9]\d{9}(?![\d.])")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

STATUS = {"open", "closed", "renovating", "under_construction", "unknown"}
STATUS_SOURCE = {
    "official_site_listed", "derived_from_hotels_asia", "third_party_listing",
    "official_site", "retired_list", "not_verified", "no_source_link",
}

# file -> (key column, required columns, numeric columns)
RULES = {
    "hotels.public.csv": (
        "id",
        ["id", "slug", "venue_type", "brand_group", "star_rating", "country",
         "geo_precision", "status", "status_source", "status_asof"],
        ["lng", "lat", "opening_year"],
    ),
    "venues.public.csv": (
        "master_id",
        ["master_id", "name_zh", "category", "country", "status", "status_source",
         "status_asof"],
        ["lng", "lat"],
    ),
    "sample-80-halls-20261027.csv": (
        "room_id",
        ["venue_id", "venue_name", "room_id", "room_name", "source_url", "data_level",
         "status", "status_asof", "updated_at"],
        ["area_sqm", "length_m", "width_m", "height_m", "capacity_banquet_pax",
         "capacity_theater_pax", "capacity_classroom_pax", "capacity_reception_pax",
         "capacity_max_pax"],
    ),
    "sample-80-venues-20261027.csv": (
        "venue_id",
        ["venue_id", "name_zh", "city", "country", "website", "updated_at", "license"],
        ["lng", "lat", "opening_year"],
    ),
    "whitelist-v2.csv": (
        "column",
        ["file", "column", "action"],
        [],
    ),
    "batch2-exhibition-centres-20261029.csv": (
        "venue_id",
        ["venue_id", "name_zh", "country", "city", "halls_count", "status", "intro_zh", "intro_en", "source"],
        ["halls_count", "halls_area_sqm"],
    ),
    "batch2-exhibition-halls-20261029.csv": (
        "hall_uid",
        ["hall_uid", "venue_id", "hall_id", "hall_name", "source_url"],
        ["area_sqm", "length_m", "width_m", "height_m", "floor_load_t_sqm"],
    ),
    "batch3-sports-arts-retail-popup-racing-20261029.csv": (
        "venue_id",
        ["group", "venue_id", "name_zh", "city", "country", "address", "intro_zh", "intro_en", "source"],
        [],
    ),
    "cases.csv": (
        "case_id",
        ["case_id", "year", "title", "lang", "source", "url"],
        [],
    ),
}


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_file(path, rule, index):
    name = os.path.basename(path)
    errs = []
    keycol, required, _numerics = rule
    meta = index.get("files", {}).get(name, {})
    schema_path = os.path.join(ROOT, meta.get("schema", "")) if meta.get("schema") else ""
    numeric_cols = set()
    if schema_path and os.path.exists(schema_path):
        schema = json.load(open(schema_path, encoding="utf-8"))
        numeric_cols = {c for c, p in schema.get("properties", {}).items()
                        if "number" in p.get("type", []) or "integer" in p.get("type", [])}

    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        errs.append(f"{name}: UTF-8 BOM present")
    if b"\r" in raw:
        errs.append(f"{name}: CRLF/CR line ending present")

    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        rows = list(reader)

    for c in required:
        if c not in cols:
            errs.append(f"{name}: missing required column `{c}`")
    if keycol not in cols:
        return errs, len(rows), len(cols)

    if name in index.get("files", {}):
        meta = index["files"][name]
        if meta["rows"] != len(rows):
            errs.append(f"{name}: rows {len(rows)} != _index {meta['rows']}")
        if meta["columns"] != len(cols):
            errs.append(f"{name}: columns {len(cols)} != _index {meta['columns']}")
        digest = sha256(path)
        if meta["sha256"] != digest:
            errs.append(f"{name}: sha256 {digest[:16]}… != _index {meta['sha256'][:16]}…")
    else:
        errs.append(f"{name}: not listed in schema/_index.json")

    seen = set()
    url_seen = set()
    venue_counts = Counter()
    for i, r in enumerate(rows, 2):
        rid = (r.get(keycol) or "").strip()
        if name == "whitelist-v2.csv":
            rid = f"{(r.get('file') or '').strip()}|{rid}"
        if not rid:
            errs.append(f"{name} L{i}: empty {keycol}")
        elif rid in seen:
            errs.append(f"{name} L{i}: duplicate {keycol} {rid}")
        else:
            seen.add(rid)

        if name == "cases.csv":
            lang = (r.get("lang") or "").strip()
            if lang not in ("zh", "en"):
                errs.append(f"{name} L{i}: bad lang {lang!r}")
            u = (r.get("url") or "").strip()
            if u:
                if u in url_seen:
                    errs.append(f"{name} L{i}: duplicate url {u}")
                url_seen.add(u)
            vid = (r.get("venue_id") or "").strip()
            if vid:
                venue_counts[vid] += 1

        for c in numeric_cols:
            v = (r.get(c) or "").strip()
            if v == "":
                continue
            try:
                float(v.replace(",", ""))
            except ValueError:
                errs.append(f"{name} L{i}: {c} not numeric: {v!r}")

        if "lng" in cols and "lat" in cols:
            lng = (r.get("lng") or "").strip()
            lat = (r.get("lat") or "").strip()
            if bool(lng) != bool(lat):
                errs.append(f"{name} L{i}: lng/lat not paired")
            if lng and lat:
                try:
                    x, y = float(lng), float(lat)
                    if not (-180 <= x <= 180 and -90 <= y <= 90) or (x == 0 and y == 0):
                        errs.append(f"{name} L{i}: coordinate out of range {lng},{lat}")
                except ValueError:
                    errs.append(f"{name} L{i}: invalid coordinate {lng},{lat}")

        if "status" in cols:
            st = (r.get("status") or "").strip()
            if st not in STATUS:
                errs.append(f"{name} L{i}: bad status {st!r}")
        if "status_source" in cols:
            ss = (r.get("status_source") or "").strip()
            if ss not in STATUS_SOURCE:
                errs.append(f"{name} L{i}: bad status_source {ss!r}")
        for c in cols:
            if c.endswith("_at") or c.endswith("_asof"):
                v = (r.get(c) or "").strip()
                if v and not DATE.match(v):
                    errs.append(f"{name} L{i}: {c} not YYYY-MM-DD: {v!r}")

        for c in cols:
            v = str(r.get(c) or "")
            if EMAIL.search(v):
                errs.append(f"{name} L{i}: email-like value in {c}")
            if PHONE.search(v):
                errs.append(f"{name} L{i}: mobile-like value in {c}")

    if name == "cases.csv":
        over = {k: v for k, v in venue_counts.items() if v > 3}
        if over:
            errs.append(f"{name}: more than 3 cases on {len(over)} venue(s): {sorted(over)[:5]}")

    return errs, len(rows), len(cols)


def main(argv):
    index = json.load(open(INDEX, encoding="utf-8")) if os.path.exists(INDEX) else {"files": {}}
    if argv:
        paths = [os.path.abspath(a) for a in argv]
    else:
        paths = [os.path.join(DATA, f) for f in sorted(os.listdir(DATA)) if f.lower().endswith(".csv")]

    all_errs = []
    total = 0
    for path in paths:
        name = os.path.basename(path)
        if name not in RULES:
            all_errs.append(f"{name}: no validation rule")
            continue
        errs, nrows, ncols = check_file(path, RULES[name], index)
        total += nrows
        all_errs.extend(errs)
        print(f"{name}: {nrows} rows × {ncols} cols, {len(errs)} error(s)")

    # every indexed data file must exist, and vice versa
    if not argv:
        on_disk = {f for f in os.listdir(DATA) if f.lower().endswith(".csv")}
        indexed = set(index.get("files", {}))
        for f in sorted(indexed - on_disk):
            all_errs.append(f"{f}: listed in _index.json but missing from data/")
        for f in sorted(on_disk - indexed):
            all_errs.append(f"{f}: present in data/ but not in _index.json")

    print(f"TOTAL: {total} rows, {len(all_errs)} error(s)")
    for e in all_errs[:60]:
        print("  E", e)
    if len(all_errs) > 60:
        print(f"  ... and {len(all_errs) - 60} more")
    return 0 if not all_errs else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
