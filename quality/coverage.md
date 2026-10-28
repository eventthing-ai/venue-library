# Data coverage

*Generated from the public CSVs by `scripts/build_coverage.py`. Do not edit by hand — run the script, or CI will flag the difference.*

A blank cell means **not published or not captured**, never `0` and never `N/A`. Coverage is per file, per column.

## `hotels.public.csv` — Public hotel inventory (4–5 star, Asia)

3038 rows · 23 columns · sha256 `b738e646c17ac497…`

| Column | Filled | Coverage |
|---|---:|---:|
| `id` | 3038 | 100.0% |
| `slug` | 3038 | 100.0% |
| `name_zh` | 1277 | 42.0% |
| `name_en` | 2643 | 87.0% |
| `venue_type` | 3038 | 100.0% |
| `brand_group` | 3038 | 100.0% |
| `brand` | 3029 | 99.7% |
| `star_rating` | 3038 | 100.0% |
| `country` | 3038 | 100.0% |
| `country_zh` | 2468 | 81.2% |
| `city` | 2954 | 97.2% |
| `city_zh` | 759 | 25.0% |
| `address_en` | 2106 | 69.3% |
| `lng` | 1492 | 49.1% |
| `lat` | 1492 | 49.1% |
| `geo_precision` | 3038 | 100.0% |
| `website` | 3037 | 100.0% |
| `updated_at` | 3038 | 100.0% |
| `license` | 3038 | 100.0% |
| `opening_year` | 64 | 2.1% |
| `status` | 3038 | 100.0% |
| `status_source` | 3038 | 100.0% |
| `status_asof` | 3038 | 100.0% |

**Coordinates:** `lng` present on 1492 of 3038 rows (49.1%). Datum is WGS-84; see `docs/coordinates.md`.

## `venues.public.csv` — Public China venue directory

3549 rows · 17 columns · sha256 `def1debe7fd7852e…`

| Column | Filled | Coverage |
|---|---:|---:|
| `master_id` | 3549 | 100.0% |
| `name_zh` | 3549 | 100.0% |
| `name_en` | 641 | 18.1% |
| `category` | 3549 | 100.0% |
| `sub_type` | 3547 | 99.9% |
| `country` | 3549 | 100.0% |
| `province` | 943 | 26.6% |
| `city` | 3515 | 99.0% |
| `district` | 908 | 25.6% |
| `address` | 3490 | 98.3% |
| `source_url` | 421 | 11.9% |
| `lng` | 656 | 18.5% |
| `lat` | 656 | 18.5% |
| `status` | 3549 | 100.0% |
| `status_source` | 3549 | 100.0% |
| `status_asof` | 3549 | 100.0% |
| `hotel_id_ref` | 441 | 12.4% |

**Coordinates:** `lng` present on 656 of 3549 rows (18.5%). Datum is WGS-84; see `docs/coordinates.md`.

## `cases.csv` — Case index (links only)

1309 rows · 14 columns · sha256 `b76264acf85e5585…`

| Column | Filled | Coverage |
|---|---:|---:|
| `case_id` | 1309 | 100.0% |
| `venue_id` | 1303 | 99.5% |
| `venue_name` | 1303 | 99.5% |
| `venue_name_en` | 1303 | 99.5% |
| `city` | 1303 | 99.5% |
| `city_en` | 1303 | 99.5% |
| `brand` | 1307 | 99.8% |
| `brand_en` | 452 | 34.5% |
| `year` | 1309 | 100.0% |
| `title` | 1309 | 100.0% |
| `lang` | 1309 | 100.0% |
| `source` | 1309 | 100.0% |
| `published_at` | 1297 | 99.1% |
| `url` | 1309 | 100.0% |

**Coordinates:** no coordinate column in this file.

## `sample-80-halls-20261027.csv` — 80-hotel hall-level sample

2100 rows · 21 columns · sha256 `50011f2cd3373d3a…`

| Column | Filled | Coverage |
|---|---:|---:|
| `venue_id` | 2100 | 100.0% |
| `venue_name` | 2100 | 100.0% |
| `city` | 2100 | 100.0% |
| `country` | 2100 | 100.0% |
| `room_id` | 2100 | 100.0% |
| `room_name` | 2100 | 100.0% |
| `area_sqm` | 2093 | 99.7% |
| `length_m` | 1058 | 50.4% |
| `width_m` | 1058 | 50.4% |
| `height_m` | 1048 | 49.9% |
| `capacity_banquet_pax` | 1317 | 62.7% |
| `capacity_theater_pax` | 1281 | 61.0% |
| `capacity_classroom_pax` | 1255 | 59.8% |
| `capacity_reception_pax` | 1280 | 61.0% |
| `capacity_max_pax` | 988 | 47.0% |
| `source_url` | 2100 | 100.0% |
| `data_level` | 2100 | 100.0% |
| `dims_qa` | 524 | 25.0% |
| `status` | 2100 | 100.0% |
| `status_asof` | 2100 | 100.0% |
| `updated_at` | 2100 | 100.0% |

**Coordinates:** no coordinate column in this file.

## `sample-80-venues-20261027.csv` — 80-hotel venue-level sample

80 rows · 15 columns · sha256 `cc77b39af8f2262f…`

| Column | Filled | Coverage |
|---|---:|---:|
| `venue_id` | 80 | 100.0% |
| `name_zh` | 80 | 100.0% |
| `name_en` | 60 | 75.0% |
| `city` | 80 | 100.0% |
| `country` | 80 | 100.0% |
| `address` | 60 | 75.0% |
| `website` | 80 | 100.0% |
| `star_rating` | 80 | 100.0% |
| `brand_group` | 80 | 100.0% |
| `brand` | 79 | 98.8% |
| `opening_year` | 0 | 0.0% |
| `lng` | 40 | 50.0% |
| `lat` | 40 | 50.0% |
| `updated_at` | 80 | 100.0% |
| `license` | 80 | 100.0% |

**Coordinates:** `lng` present on 40 of 80 rows (50.0%). Datum is WGS-84; see `docs/coordinates.md`.

## `batch2-exhibition-centres-20261029.csv` — Batch 2 — exhibition centres (Asia)

104 rows · 13 columns · sha256 `29edbecb5bd44197…`

| Column | Filled | Coverage |
|---|---:|---:|
| `venue_id` | 104 | 100.0% |
| `name_zh` | 104 | 100.0% |
| `country` | 104 | 100.0% |
| `city` | 104 | 100.0% |
| `address` | 98 | 94.2% |
| `website` | 90 | 86.5% |
| `halls_count` | 104 | 100.0% |
| `halls_area_sqm` | 82 | 78.8% |
| `status` | 104 | 100.0% |
| `status_note` | 104 | 100.0% |
| `intro_zh` | 41 | 39.4% |
| `intro_en` | 104 | 100.0% |
| `source` | 104 | 100.0% |

**Coordinates:** no coordinate column in this file.

## `batch2-exhibition-halls-20261029.csv` — Batch 2 — exhibition halls

797 rows · 13 columns · sha256 `8553a1d3be4396ef…`

| Column | Filled | Coverage |
|---|---:|---:|
| `hall_uid` | 797 | 100.0% |
| `venue_id` | 797 | 100.0% |
| `venue_name` | 797 | 100.0% |
| `hall_id` | 797 | 100.0% |
| `hall_name` | 797 | 100.0% |
| `area_sqm` | 632 | 79.3% |
| `length_m` | 359 | 45.0% |
| `width_m` | 360 | 45.2% |
| `height_m` | 607 | 76.2% |
| `floor_load_t_sqm` | 486 | 61.0% |
| `pillar_free` | 192 | 24.1% |
| `source_url` | 797 | 100.0% |
| `note` | 780 | 97.9% |

**Coordinates:** no coordinate column in this file.

## `batch3-sports-arts-retail-popup-racing-20261029.csv` — Batch 3 — sports, arts, retail & pop-up, racing

559 rows · 15 columns · sha256 `a585f1bdecb4aeba…`

| Column | Filled | Coverage |
|---|---:|---:|
| `group` | 559 | 100.0% |
| `venue_id` | 559 | 100.0% |
| `name_zh` | 559 | 100.0% |
| `city` | 558 | 99.8% |
| `country` | 559 | 100.0% |
| `address` | 556 | 99.5% |
| `website` | 491 | 87.8% |
| `area_text` | 487 | 87.1% |
| `capacity_text` | 330 | 59.0% |
| `open_year` | 214 | 38.3% |
| `status` | 559 | 100.0% |
| `status_note` | 22 | 3.9% |
| `intro_zh` | 489 | 87.5% |
| `intro_en` | 489 | 87.5% |
| `source` | 489 | 87.5% |

**Coordinates:** no coordinate column in this file.

## `whitelist-v2.csv` — Public-layer column whitelist

113 rows · 4 columns · sha256 `35a32a281ed7dc6a…`

| Column | Filled | Coverage |
|---|---:|---:|
| `file` | 113 | 100.0% |
| `column` | 113 | 100.0% |
| `action` | 113 | 100.0% |
| `note` | 80 | 70.8% |

**Coordinates:** no coordinate column in this file.

## Summary

| File | Rows | Columns | Coordinates | sha256 |
|---|---:|---:|---:|---|
| `hotels.public.csv` | 3038 | 23 | 49.1% | `b738e646c17ac497…` |
| `venues.public.csv` | 3549 | 17 | 18.5% | `def1debe7fd7852e…` |
| `cases.csv` | 1309 | 14 | — | `b76264acf85e5585…` |
| `sample-80-halls-20261027.csv` | 2100 | 21 | — | `50011f2cd3373d3a…` |
| `sample-80-venues-20261027.csv` | 80 | 15 | 50.0% | `cc77b39af8f2262f…` |
| `batch2-exhibition-centres-20261029.csv` | 104 | 13 | — | `29edbecb5bd44197…` |
| `batch2-exhibition-halls-20261029.csv` | 797 | 13 | — | `8553a1d3be4396ef…` |
| `batch3-sports-arts-retail-popup-racing-20261029.csv` | 559 | 15 | — | `a585f1bdecb4aeba…` |
| `whitelist-v2.csv` | 113 | 4 | — | `35a32a281ed7dc6a…` |

*EVENTTHING · Hong Kong · venue.eventthing.ai*
