# CHANGELOG

Version numbers follow the public release (`v1.0.x`). The repository content is the public layer:
a directory plus schema, not the internal masters.

## 2026-10-28 — case index added; 39 hall dimensions restored

### Data

- **`data/cases.csv`** — new: **1,309 rows × 14 columns**. 1,303 rows carry a venue ID
  (525 venues, up to 3 cases each; 1,300 join `venues.public.csv`), 6 are media pages without a
  venue. Each row carries a title, brand, year, publisher and a **link to the original**; no body
  text. Coverage 2015–2026.
- **`data/sample-80-halls-20261027.csv`** — 2,100 rows; **1,039 rows with full
  length/width/height** (was 1,005). The 39 rows previously blanked keep their area and now publish
  length/width/height as recorded, flagged `dims_qa=area_dims_conflict` (caliber difference, not a
  data error).

### Documentation and tooling

- README (EN/ZH/FR), llms.txt, CREDITS, fields.md, schema/_index.json, schema/cases.schema.json and
  data/manifest.json updated for the case index and the restored counts.
- `scripts/field_meta.py` now defines `cases.csv`; `gen_schema.py`, `gen_fields_md.py` and
  `build_coverage.py` include it.
- `validate.py` adds case checks: language vocabulary, unique URL, max 3 cases per venue.

## 2026-10-27 — hall sample expanded: 60 → 80 hotels (Hilton group added)

### Data

- **`data/sample-80-halls-20261027.csv`** — **2,100 rows** (was 1,615), **80 hotels** (was 60).
  New fourth group: **20 Hilton hotels in China, 485 halls**, parsed from their official
  hilton.com event pages (fetched 2026-10-25). Source pages publish area and seven layout
  capacities but **no length/width/height** — those three columns stay blank and are flagged
  `dims_qa=source_no_dims` (a new value; `area_dims_conflict` keeps its old meaning). Of the seven
  layouts, four enter the public columns (banquet / theatre / classroom / reception) plus
  `capacity_max_pax`; u-shape, conference and square stay internal. 17 rows below 10 sqm
  (meeting pods, not halls) were dropped.
- **`data/sample-80-venues-20261027.csv`** — 80 rows × 15 columns (was 60).
- Both sample files renamed (60-venue sample → 80-venue sample, 2026-10-27); every reference in
  README, llms.txt, fields.md, schema, validate.py and the coverage report updated.
- Directory totals unchanged: 3,549 venues × 17, 3,038 hotels × 23, 441 cross-references,
  main count **6,146**.

## 2026-10-26 — public projection freeze (repo now ships public files only)

### Data

- **`data/hotels.public.csv`** — 3,038 rows × 23 columns. 4–5 star hotels across Asia; identity,
  brand, star rating, country/city, address, coordinates where published, official website, opening
  year, and `status` / `status_source` / `status_asof`. One five-star row (`WYN-febd0399`) is
  quarantined because its source record embedded a mobile number and an email address in the
  city/website fields.
- **`data/venues.public.csv`** — 3,549 rows × 17 columns. China venue directory with category,
  sub-type, province/city/district, address, source link where policy allows, coordinates where
  publishable, and status. Status: open 559 / closed 2 / unknown 2,988.
- **`data/sample-80-halls-20261027.csv`** — 2,100 rows × 21 columns. Hall-level sample; 1,039 rows
  with full length/width/height; source URL on every row.
- **`data/sample-80-venues-20261027.csv`** — 80 rows × 15 columns. Venue-level sample.
- **`data/whitelist-v2.csv`** — 72 rules (40 keep / 32 strip) recording how the public projections
  were cut from the internal masters.
- **`data/stadiums.csv`**, **`data/malls.csv`**, **`data/exhibition-centres.csv`**,
  **`data/scenic-sites.csv`** — removed from the public repository on 2026-10-26 and kept in a
  private archive; they are outside the China + Asia directory layer and are not shipped in v1.0.1.
- **Internal masters removed from the repository:** `hotels-asia.csv` (43 columns) and
  `venues.csv` (22 columns) now live outside the public repo. They are not published, not linked,
  and not required to read any public file.

### Documentation and tooling

- `fields.md` regenerated for the public layer: 23 / 16 / 21 / 15 columns, English, Chinese and
  French, including the `status` vocabulary and the `unknown` rule.
- `schema/` regenerated from the public CSVs: five schemas plus `_index.json` with current row
  counts and SHA-256. `schema/hotels-asia.schema.json` and `schema/venues.schema.json` are replaced
  by `schema/hotels.public.schema.json` and `schema/venues.public.schema.json`.
- `quality/coverage.md` regenerated from the public CSVs.
- `README.md` / `README.zh.md` / `README.fr.md` rewritten for the public directory layer: 6,146
  distinct properties (3,038 + 3,549 − 441), status semantics, coordinate coverage, and what is
  deliberately withheld.
- `docs/coordinates.md` rewritten: WGS-84 rule, public coverage per file, and the meaning of a blank
  coordinate. Per-row provenance columns are internal and not published.
- `llms.txt` updated for AI crawlers.
- Added `scripts/field_meta.py`, `scripts/gen_fields_md.py`, `scripts/gen_schema.py` and
  `scripts/build_coverage.py` so the field dictionary, schema and coverage files can be regenerated
  and checked (`--check`).
- `validate.py` rewritten to validate the public files; `validate_hotels.py` retired.

### Why

The previous repository shipped internal working tables and documented 43-column / 22-column
masters that were no longer the public product. A reader could not validate a public CSV against
the published schema. This release makes the repository self-consistent: every file in `data/` has
a schema, a field entry, a coverage line, and a row count that matches `_index.json`.

---

## v1.0.1 — 29 October 2026 — public directory layer

- v1.0.1 — moved out 4 v0.9.x global reference files (stadiums/malls/exhibition-centres/scenic-sites); out of scope for the China + Asia directory layer. They are kept in a private archive and not shipped.
- 3,549 China venues × 17 columns.
- 3,038 Asia 4–5 star hotels × 23 columns.
- 80-hotel samples: 2,100 halls × 21 columns, 60 venues × 15 columns.
- Public main count: 6,146 distinct properties (441 hotel–venue cross-references).
- Status is given only where a source is held: 559 of 3,549 venues (16%); every row names its
  source type. `unknown` is not counted as open.
- Hall-level detail for the full hotel set is served through the API, not published in the open CSV.

## v1.0.0 — 29 October 2026 — hotel directory

- First public release: 3,038 four- and five-star hotels across Asia.
- The 1,246 three-star records used as the internal denominator are not published.
- Meeting-room counts, areas and capacities are not part of the open hotel CSV; the 80-hotel sample
  documents the field semantics at hall level.

## Earlier drafts

Earlier internal drafts (v0.9.x) were working packages, not public releases. They are not part of
this repository.
