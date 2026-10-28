#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate JSON Schema (draft 2020-12) and schema/_index.json from the public CSVs in data/.

Field names, types, units and descriptions come from scripts/field_meta.py, so docs, schema and
data stay in one place. A CSV whose columns do not match field_meta fails loudly; no half-built
schema is ever written.

Usage:
  python3 scripts/gen_schema.py            # generate
  python3 scripts/gen_schema.py --check    # verify only (CI)
"""
import csv
import hashlib
import json
import os
import sys

from field_meta import FILES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "schema")

RELEASE = "v1.0.1 (2026-10-29)"
SCHEMA_BASE = "https://eventthings.ai/schema/"

# Per-column type and range rules
LNG = {"lng", "geo_lon", "lon"}
LAT = {"lat", "geo_lat"}
NON_NEGATIVE = {"area_sqm", "length_m", "width_m", "height_m", "halls_area_sqm", "floor_load_t_sqm",
                "capacity_banquet_pax", "capacity_theater_pax", "capacity_classroom_pax",
                "capacity_reception_pax", "capacity_max_pax"}
YEAR_COLS = {"opening_year", "year"}


def die(msg):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(1)


def read_csv(path):
    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        die(f"{path} has a BOM; public files must be UTF-8 without BOM")
    if b"\r\n" in raw:
        die(f"{path} uses CRLF; public files must use LF")
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        rows = list(reader)
    return cols, rows, raw


def prop(col, ctype, unit, en, values=None):
    p = {"title": col, "x-unit": unit, "description": en}
    if ctype == "string":
        p["type"] = ["string", "null"]
    elif ctype == "integer":
        p["type"] = ["integer", "null"]
    elif ctype == "number":
        p["type"] = ["number", "null"]
    elif ctype == "date":
        p["type"] = ["string", "null"]
        p["format"] = "date"
        p["pattern"] = r"^\d{4}-\d{2}-\d{2}$"
    elif ctype == "enum":
        p["type"] = ["string", "null"]
        p["enum"] = list(values or []) + [None]
    else:
        die(f"{col}: unknown type {ctype}")

    if col in LNG:
        p.update({"minimum": -180, "maximum": 180})
    elif col in LAT:
        p.update({"minimum": -90, "maximum": 90})
    elif col in NON_NEGATIVE:
        p["minimum"] = 0
    elif col == "star_rating":
        p.update({"minimum": 1, "maximum": 5})
    elif col in YEAR_COLS:
        p.update({"minimum": 1800, "maximum": 2100})
    elif col == "rank":
        p["minimum"] = 1
    return p


def build(spec):
    path = os.path.join(DATA, spec["file"])
    if not os.path.exists(path):
        die(f"missing file {path}")
    cols, rows, raw = read_csv(path)
    meta_cols = [c[0] for c in spec["columns"]]
    if cols != meta_cols:
        die(f"{spec['file']} column mismatch\n  data: {cols}\n  dictionary: {meta_cols}")

    props = {}
    for col, ctype, unit, en, *rest in spec["columns"]:
        props[col] = prop(col, ctype, unit, en, rest[0] if rest else None)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_BASE + spec["schema"],
        "title": f"EVENTTHING Venue Library — {spec['file']}",
        "description": (
            f"One record of `data/{spec['file']}` ({len(rows):,} rows, {len(cols)} columns). "
            "Empty CSV cells are `null`; numbers are stored as CSV text and MUST be coerced "
            "before validation. Encoding: UTF-8 without BOM, LF. See `fields.md`."
        ),
        "type": "object",
        "additionalProperties": False,
        "properties": props,
        "required": spec["required"],
        "x-primary-key": spec["pk"],
        "x-release": RELEASE,
        "x-row-count": len(rows),
        "x-column-count": len(cols),
        "x-sha256": hashlib.sha256(raw).hexdigest(),
    }
    return schema


def main(check=False):
    os.makedirs(OUT, exist_ok=True)
    index = {
        "release": RELEASE,
        "generated_from": "data",
        "rules": {"encoding": "UTF-8 no BOM", "lineending": "LF",
                  "empty": "empty CSV cell = null"},
        "files": {},
    }
    changed = []
    for spec in FILES:
        schema = build(spec)
        text = json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
        out = os.path.join(OUT, spec["schema"])
        old = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
        if old != text:
            changed.append(spec["schema"])
            if not check:
                with open(out, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text)
        index["files"][spec["file"]] = {
            "schema": f"schema/{spec['schema']}",
            "rows": schema["x-row-count"],
            "columns": schema["x-column-count"],
            "primary_key": spec["pk"],
            "sha256": schema["x-sha256"],
        }
    index["files"] = dict(sorted(index["files"].items()))

    idx_text = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    idx_path = os.path.join(OUT, "_index.json")
    old = open(idx_path, encoding="utf-8").read() if os.path.exists(idx_path) else ""
    if old != idx_text:
        changed.append("_index.json")
        if not check:
            with open(idx_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(idx_text)

    if check:
        if changed:
            print("SCHEMA STALE:", ", ".join(changed))
            sys.exit(1)
        print("schema up to date")
    else:
        print("schema written:", ", ".join(changed) or "no change")
        for fn, meta in index["files"].items():
            print(f"  {fn}: {meta['rows']} × {meta['columns']}  sha {meta['sha256'][:16]}")


if __name__ == "__main__":
    main("--check" in sys.argv)
