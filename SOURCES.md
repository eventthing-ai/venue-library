# Sources and provenance

Every value in this repository is traceable to a public source. This file explains which kinds of
sources we use, what each source type means, and the rules we apply when a source is a directory
rather than the venue itself.

> **Public projection note (2026-10-26).** The public CSVs carry only the columns listed in
> `fields.md`. Provenance and internal scoring columns — `source_type`, `data_origin`,
> `case_count`, `coord_source`, `coord_grade`, `coord_check_m` — are retained internally and are
> not part of the public files. This document describes the rules behind the data, not additional
> columns a reader will find in every CSV.

---

## 1. Source hierarchy

We prefer sources in this order. A record is only as strong as the level it comes from.

| Level | Source | Where it appears |
|---|---|---|
| **1** | The venue's own official website — venue pages, floor plans, fact sheets, capacity charts | `source_type = official_site`, `source_ref = <venue URL>` |
| **2** | The owning group's official site (hotel group, exhibition group, mall operator) | `source_type = official_site`, `source_ref = <group URL>` |
| **3** | National / regional industry bodies and venue associations — e.g. convention-bureau venue directories, national exhibition-association member lists, municipal government venue registries | `source_type = official_directory`, `source_ref = <directory URL>` |
| **4** | Public reference records — government planning documents, open data portals, OpenStreetMap | `data_origin = public_web`, `source_ref = <URL>` |
| **5** | Trade directories and press — used only when levels 1–4 have nothing, and always as a pointer, not as the final word | `source_type = directory`, `source_ref = <URL>` |

**Levels 1–3 are the backbone.** Directory data (level 5) is never used for facts that a venue
publishes itself (areas, capacities, dimensions) unless the venue has no such page.

## 2. What `data_origin` means

| Value | Meaning |
|---|---|
| `own_addr_book` | Our own venue book, built over years of project work and cross-checked against venue pages |
| `official_site_crawl` | Read from the venue's or group's official site |
| `public_web` | A public reference source (government page, open data, OpenStreetMap) |
| `partner` | Supplied by a partner or the venue directly |
| `community` | A contribution via pull request, reviewed before merge |

## 3. Coordinates

Coordinates are never taken on trust from a directory without a datum. Chinese sources are
converted from GCJ-02 or BD-09 to WGS-84, and every row says which pipeline produced it
(`coord_source`) plus a confidence grade. Details and measured accuracy:
[`docs/coordinates.md`](docs/coordinates.md).

## 4. Case counts

`case_count` and the `top_brands` / `top_agencies` columns come from **onsiteclub.com**, our own
case archive of brand activations and pop-ups. They are counts of published cases, not of all
activity that ever happened at a venue. These columns are internal-only and are **not** part of the
public venue CSV. A separate public file, `data/cases.csv`, lists up to three cases per venue as
title, brand, year, publisher and a **link to the original**; it contains no body text and does not
redistribute the case archive itself.

## 5. Rights

- **Facts are not copyrightable**; we republish facts (names, addresses, published areas, capacities).
- **We do not copy prose.** Descriptions in this repository are written by us from the facts, not
  pasted from Wikipedia (CC BY-SA) or from venue marketing copy.
- **We do not redistribute directories.** Where a directory was used to *find* a venue, the row
  records the venue's own page as `source_ref`, not the directory's page.
- **Images** are not part of this dataset. Where an image is added in future it carries its own
  licence field; nothing is taken from a venue's site without permission.

## 6. Corrections

If a source was misread, open an issue with the field, the current value, the correct value and the
source. Corrections are logged in `CHANGELOG.md` — including ours.

*EVENTTHING · Hong Kong · venue.eventthing.ai*
