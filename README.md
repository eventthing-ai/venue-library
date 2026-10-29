# EVENTTHING Venue Library

**Open venue data for experiential marketing — starting from East Asia.**

East Asia is the most active experiential marketing market in the world, especially for fast-moving consumer goods (FMCG). Brand activations, pop-ups and venue-based campaigns launch here at a pace and density found nowhere else. This dataset starts here because this is where the demand is.

Built for multilingual teams and FMCG marketing — not a tech-product database.

**Current public release: `v1.0.1` (29 October 2026) — public directory layer: 3,549 China venues and 3,038 Asia 4–5 star hotels, plus two sample files in four depth groups.**

---

## What this is

An information service: a website, a URL, a structured dataset. Not a phone number, not a human middleman.

As AI-to-AI communication and autonomous contracting mature, human intervention decreases and efficiency rises. That is the direction this dataset is built for: we want a brand's marketing AI to connect directly with a hotel's sales AI, so both sides can complete more tasks, compare rates, and find the right venue faster, with this library as the comparison layer.

**This repository is one part of what EVENTTHING shows publicly.** Consulting is also part of our business; the open-source dataset is the public layer, not the whole company. The open layer is the directory and the schema. Hall-level detail for the full hotel set — dimensions, ceiling height, layout capacities, floor load — is served through our API; only the two display samples are published openly.

---

## Where we are

EVENTTHING is based in Hong Kong. We start from Asia — the most advanced offline marketing market — because that is where the practice is furthest ahead.

A large part of the Asian venue and case information comes from our own network, including onsiteclub.com, and is used here as structured reference data.

---


## What ships, in three batches

The 29 October release is published in three batches. Together they cover the full library.

| Batch | Type | With full content | Library total |
|---|---|---:|---:|
| 1 | Hotels (4–5 star, Asia) | 80 | 3,038 |
| 2 | Exhibition centres | 93 | 104 |
| 3 | Sports venues | 273 | 273 |
| 3 | Arts venues | 124 | 124 |
| 3 | Retail and pop-up spaces (94 malls + 54 pop-up spaces) | 148 | 2,546 |
| 3 | Racing circuits | 14 | 14 |

> Sports rows in the source table included 14 racing circuits; they are counted once, under Racing circuits, so the two lines still add up to the original 287.

Hotels beyond the 80 samples, and every other venue outside the counts above, are published as **name-only** entries until their full record is verified. Hall-level detail ships for 80 hotels (2,100 halls) and 104 exhibition centres (797 halls); every row carries a source URL.

## Browse by category — the same eight views as the web version

The library is published as one set with eight views. Every view is a filter over the same CSV files; the counts below are for this release.

| View | Records | What it covers | Files |
|---|---:|---|---|
| **Hotel** | 3,038 | 4–5 star hotels across Asia. 2,643 carry an official English name; the remaining 395 are name-pending and are listed in the data only under their local name | `data/hotels.public.csv` |
| **All Venue** | 3,549 | The China venue directory — one row per venue, every category | `data/venues.public.csv` |
| **Shop Mall** | 2,557 | Shopping malls 2,463 (venue directory) + 94 retail formats | `data/venues.public.csv`, `data/batch3-sports-arts-retail-popup-racing-20261029.csv` |
| **Art Museum** | 127 | Art museums and art spaces 124 + performing-arts venues 3 | `data/batch3-…csv`, `data/venues.public.csv` |
| **Exhibition** | 933 | 104 exhibition centres + 797 halls + 32 venue-level rows | `data/batch2-…csv`, `data/venues.public.csv` |
| **Sports** | 338 | 273 sports venues + 14 racing circuits + 51 venue-level rows | `data/batch3-…csv`, `data/venues.public.csv` |
| **POP-UP** | 54 | Pop-up spaces — malls, streets and cultural districts used for pop-ups | `data/batch3-…csv` |
| **CASES** | 1,309 | Case index, up to 3 cases per venue, link-only | `data/cases.csv` |

The views overlap by design: **All Venue** contains every venue row (including the 452 hotel-category rows), and Shop Mall / Art Museum / Exhibition / Sports / POP-UP are subsets of it. Counts are per view and are not meant to add up.

The web version of the library presents the same eight views, and its Cases view also lists 3,492 pop-up gallery records from 10,000POP as a connected index. Those gallery records are **not** part of this CSV release; only `data/cases.csv` ships here.

## What's inside

| File | Rows × columns | What it is |
|---|---:|---|
| `data/hotels.public.csv` | 3,038 × 23 | **4–5 star hotels across Asia**: name, brand group and brand, star rating, country/city, address, coordinates where we hold a WGS-84 pair, official website, status |
| `data/venues.public.csv` | 3,549 × 17 | **China venue directory**: name, category and sub-type, province/city/district, address, source link where policy allows, coordinates where policy allows, status, and `hotel_id_ref` (the 441 rows that also appear in the hotel file) |
| `data/cases.csv` | 1,309 × 14 | **Case index**: up to 3 cases per venue; venue ID / venue / city / brand / year / title / source / date / **link to the original** (links only, no body text) |
| `data/sample-80-venues-20261027.csv` | 80 × 15 | Sample file 1 — venue-level records for the 80-hotel sample (a display sample, not a data file) |
| `data/sample-80-halls-20261027.csv` | 2,100 × 21 | Sample file 2 — **hall-level sample in four depth groups**: area, length, width, ceiling height, four layout capacities plus maximum, and a source URL on every row. 1,039 rows have full length/width/height |
| `data/README-samples.md` | — | Sample-file notes: the four depth groups, the 21 fields and the quality rules applied |
| `data/STATUS.md` | — | Status coverage by source type and the verification plan |
| `data/whitelist-v2.csv` | 113 × 4 | Column whitelist: which columns are published, which are withheld, and why — including the Batch 2 and Batch 3 public files |
| `data/batch2-exhibition-centres-20261029.csv` | 104 × 13 | **Batch 2 — exhibition centres**: name, country, city, address, official website, number of halls, hall area total, status and status note, full EN and ZH profile text, source |
| `data/batch2-exhibition-halls-20261029.csv` | 797 × 13 | **Batch 2 — exhibition halls**: composite hall ID, one row per hall with area, length, width, ceiling height, floor load, column-free flag, source URL and notes |
| `data/batch3-sports-arts-retail-popup-racing-20261029.csv` | 559 × 15 | **Batch 3 — sports, arts, retail & pop-up, racing**: group tag, venue identity, address, website, area/capacity text, opening year, status and status note, EN and ZH profile text, source |
| `data/manifest.json` | — | Build manifest: rows, columns, SHA-256, quarantine record and source hashes |
| `fields.md` | — | Field dictionary: every column, unit and convention (EN / ZH / FR) |
| `schema/` | — | JSON Schemas (draft 2020-12), one per file, plus `_index.json` with row counts and SHA-256 |
| `docs/coordinates.md` | — | WGS-84 rule, coverage, and what a blank coordinate means |
| `quality/coverage.md` | — | Per-column fill rates, generated from the data |
| `SOURCES.md` | — | Source hierarchy and provenance rules |
| `CONTRIBUTING.md` | — | How to submit a correction or a new venue |
| `CREDITS.md` | — | Sources and credits |
| `CHANGELOG.md` | — | What changed in each release |

**Public count.** 3,038 hotels + 3,549 venues − 441 cross-references = **6,146 distinct properties**. To reproduce it: join `venues.public.csv.hotel_id_ref` (non-empty on 441 rows) to `hotels.public.csv.id`. The two sample files are **display samples**, not data files: they are subsets of the hotel inventory and are not added to this count.

**Not in the public layer:** phone numbers, contact persons, personal email addresses, pricing, and meeting-room/area/capacity fields for the full hotel set. The 80-hotel sample shows those field semantics at hall level; the full hall table stays behind the API. Commercial-category source links are withheld by policy: `source_url` is present on 421 of 3,549 venue rows (11.9%), and for the 102 venues marked `open` from a third-party listing the evidence stays internal.

---

## Cases

`data/cases.csv` is our case index: 1,309 links in total (2015–2026), of which 1,303 are attached to 525 venues (up to 3 per venue) and 6 are media pages without a venue. Each row carries only the title, brand, year, publisher and a **link to the original** — no body text; readers follow the link back to the source. Nothing is reproduced beyond the title, and every venue can show what has actually been staged there.

## Status: open, closed, unknown

Every hotel and venue row carries `status`, `status_source` and `status_asof`.

- **Hotels:** all 3,038 rows are `open` with `status_source = official_site_listed` — the property was listed on its brand's official site at build time. This is a listing signal, not a site visit.
- **Venues:** `status` is given only where we hold a source: **559 of 3,549 (16%)** are `open` — 441 `derived_from_hotels_asia`, 102 `third_party_listing`, 16 `official_site` — 2 are `closed`, and **2,988 are `unknown`**. Every row names its `status_source`; `unknown` means **not verified** and is not treated as open.
- **Third-party listings:** 102 venues are `open` on the strength of a third-party listing whose link is withheld by policy. The evidence stays internal, so an `open` row without a `source_url` is expected in those cases.
- **Samples:** the hall sample carries `status` and `status_asof` but not `status_source`; the venue-level sample carries no status column. The two main tables carry all three columns.

---

## Coordinates

Chinese venue data circulates in three coordinate systems — WGS-84 (GPS / OpenStreetMap), GCJ-02 (Chinese map providers) and BD-09 (Baidu) — each roughly 500 metres from the next. Mixing them quietly puts a venue on the wrong block.

This dataset publishes **WGS-84 only**. Coordinates are provided where we hold a WGS-84 pair (49.1% of hotels, 18.5% of venues); commercial venues carry none by policy:

- hotels: 1,492 of 3,038 (49.1%)
- venues: 656 of 3,549 (18.5%) — commercial-category coordinates are withheld by policy
- 80-hotel sample: 40 of 80

Blank means **no trustworthy point**; nothing is interpolated and no city centre is used as a substitute. Full rule: [`docs/coordinates.md`](docs/coordinates.md).

---

## Area and dimensions

**`area_sqm` and `length_m` × `width_m` are two different sets of numbers. Neither is derived from the other.**

- `area_sqm` = the **published area** of the hall. What it covers depends on the venue: usually the **net exhibition area** (the floor actually usable for stands); for multi-storey halls it is the **sum of the floors**, and some include seating decks or pre-function space.
- `length_m` / `width_m` = the **building outline** of the hall (wall to wall, centre lines), which includes walls, columns, plant rooms, back-of-house and circulation.
- So an area **larger or smaller** than length × width is normal: in a single-storey hall the outline exceeds the exhibition area; in a two-storey or seated hall the area adds up the floors and exceeds the single-floor outline. **Never marked wrong, never adjusted**, and never used to compute one from the other.
- Example: Linyi International Convention & Exhibition Center, Hall 1 — 20,000 m² exhibition area with a 250 × 108 m outline; Hall 2 — 40,000 m² is the **sum of two floors**, outline 258 × 120 m. Both directions come from the same official description.
- Where a value is not published it stays blank: no interpolation, no filling one from the other.

## Star rating

Hotels are collected at three stars and above; only **four- and five-star** properties appear in the public file. The 1,246 three-star records remain in the internal denominator and are not published. `star_rating` is inferred from public information, not an official group rating.

---

## Built to be found

This dataset is built to be found — by search engines and by AI crawlers. Every file, field name and page is structured so that a query about a venue, a city or a brand can surface the right record from GitHub and from venue.eventthing.ai.

`llms.txt` is written for AI agents and lists every file and schema in one place.

---

## Contribute

GitHub is not the product. It is a standard, a method, and a proposal.

We invite agencies, venues and brands to contribute their own venue resources under the same schema, so the whole industry works from one shared map.

Run the checks listed in `CONTRIBUTING.md` before opening a pull request. A PR that fails validation will not be merged.

---

## More than data

For anyone exploring venues in mainland China or worldwide, we offer more than data: through our network, we can help you open a direct conversation with the venue.

---

## License

Data: CC BY 4.0 · Code: MIT

---

*EVENTTHING · Hong Kong · venue.eventthing.ai*
