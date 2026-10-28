# Field dictionary · public data release v1.0.1 (2026-10-29)

Every column of every CSV in this repository, documented in English. Units are shown per column; the CSV itself stores numbers only.

## Files in this release

Release `v1.0.1 (2026-10-29)` · encoding UTF-8 without BOM · LF line endings · one header row per file.

| File | Rows | Columns | Primary key | Schema |
|---|---|---|---|---|
| `hotels.public.csv` | 3,038 | 23 | `id` | [`schema/hotels.public.schema.json`](schema/hotels.public.schema.json) |
| `venues.public.csv` | 3,549 | 17 | `master_id` | [`schema/venues.public.schema.json`](schema/venues.public.schema.json) |
| `cases.csv` | 1,309 | 14 | `case_id` | [`schema/cases.schema.json`](schema/cases.schema.json) |
| `sample-80-halls-20261027.csv` | 2,100 | 21 | `room_id` | [`schema/sample-80-halls.schema.json`](schema/sample-80-halls.schema.json) |
| `sample-80-venues-20261027.csv` | 80 | 15 | `venue_id` | [`schema/sample-80-venues.schema.json`](schema/sample-80-venues.schema.json) |
| `whitelist-v2.csv` | 113 | 4 | `column` | [`schema/whitelist-v2.schema.json`](schema/whitelist-v2.schema.json) |
| `batch2-exhibition-centres-20261029.csv` | 104 | 13 | `venue_id` | [`schema/batch2-exhibition-venues.schema.json`](schema/batch2-exhibition-venues.schema.json) |
| `batch2-exhibition-halls-20261029.csv` | 797 | 13 | `hall_uid` | [`schema/batch2-exhibition-halls.schema.json`](schema/batch2-exhibition-halls.schema.json) |
| `batch3-sports-arts-retail-popup-racing-20261029.csv` | 559 | 15 | `venue_id` | [`schema/batch3-sports-arts-retail-racing.schema.json`](schema/batch3-sports-arts-retail-racing.schema.json) |

`data/whitelist-v2.csv` is release metadata (which source columns are kept or withheld and why), not a dataset; it is indexed and schema-checked like every other CSV so the contract is complete.

## Format rules

- **UTF-8, no BOM; LF line endings.** Commas separate fields; the first row is the header.
- **Empty means unpublished.** An empty cell is `null` — never `0`, never `"N/A"`, never a guess.
- **Numbers carry no units** and no thousands separators. Parse them as numbers.
- **Coordinates are WGS-84** (EPSG:4326), in decimal degrees; blank when no trustworthy point exists.
- **No contact data.** No email addresses, phone numbers or personal names are published.

## Status model

`status` answers one question: **is this venue operating?** It is evidence-based and is never defaulted to `open`.

| Value | Meaning | How it is established |
|---|---|---|
| `open` | Operating | Official site or booking page currently lists it, or an official event announcement within the last 12 months. |
| `closed` | Closed / demolished | Official notice, government release or authoritative media; or the official site is permanently offline with no successor. |
| `renovating` | Closed for renovation | Official notice of closure/refurbishment with a reopening date. |
| `under_construction` | Under construction / not yet open | Official statement that the venue is under construction or opening in a stated year. |
| `unknown` | Not verified | No usable evidence. **Not** a synonym for closed. |

**Rules**

1. Missing evidence is `unknown`, never `open`.
2. `unknown` is excluded from every “open” count (README, marketing copy, derived statistics).
3. `status_asof` is the date of the evidence, not the date the file was built.
4. Status belongs to the venue. Halls in the sample inherit the status of their hotel.
5. `status_source` names the evidence type; a row with `status=open` always carries one.

| `status_source` | Used in | Meaning |
|---|---|---|
| `official_site_listed` | hotels.public.csv | The brand's official booking site lists the property as bookable on `status_asof`. |
| `official_site` | venues.public.csv | The venue's own official page shows it operating. |
| `derived_from_hotels_asia` | venues.public.csv | Venue matched to a hotel record whose official site lists it (`venue_id_ref`). |
| `third_party_listing` | venues.public.csv | A third-party listing page showed it available; the link itself is withheld by policy. |
| `retired_list` | venues.public.csv | Listed on the internal retired-venue list → `closed`. |
| `not_verified` | venues.public.csv | No check performed → `unknown`. |
| `no_source_link` | venues.public.csv | Previously marked open but no source link survived policy screening → downgraded to `unknown`. |

### Status in this release

| File | Rows | open | closed | renovating | under_construction | unknown |
|---|---|---|---|---|---|---|
| `hotels.public.csv` | 3,038 | 3,038 | 0 | 0 | 0 | 0 |
| `venues.public.csv` | 3,549 | 559 | 2 | 0 | 0 | 2,988 |
| `sample-80-halls-20261027.csv` | 2,100 | 2,100 | 0 | 0 | 0 | 0 |
| `sample-80-venues-20261027.csv` | 80 | — | — | — | — | — |

The two main tables are data files: every row carries `status`, `status_source` and `status_asof`. The hall sample is a display sample and carries `status` and `status_asof` only (its evidence type is the same as the hotel main table: brand official site, listed for sale on 2026-10-26). The venue-level sample is a directory sample and carries no status column at all.

## 1. `hotels.public.csv` — 23 columns

4–5 star hotels with meeting facilities across Asia — one row per property. **3,038 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `id` | string | — | Unique record ID. Prefix: ACC-* Accor, MAR-* Marriott, SHL-* Shangri-La, WYN-* Wyndham, HIL-* Hilton, IHG-* IHG. Primary key. |
| `slug` | string | — | URL-safe identifier: lowercase letters, digits and hyphens; unique within the file. |
| `name_zh` | string | — | Chinese property name as published by the hotel; blank when the source publishes no Chinese name — never machine-translated. |
| `name_en` | string | — | English property name as currently used on the official site; blank when the source publishes none. |
| `venue_type` | string | — | Always `酒店会议设施` (hotel with meeting facilities) in this file. |
| `brand_group` | string | — | Brand group: Accor / Marriott / Shangri-La / Hilton Worldwide / Wyndham Hotels & Resorts / IHG. |
| `brand` | string | — | Brand within the group (e.g. Novotel, W Hotels); official spelling kept. |
| `star_rating` | integer | stars | 4 or 5. Only 4–5 star properties are published; 3-star records stay in the internal master as denominator data. |
| `country` | string | — | Country or territory in English; Hong Kong, Macau and Taiwan are recorded separately. |
| `country_zh` | string | — | Country or territory in Chinese; blank when no official Chinese name. |
| `city` | string | — | City in English, as given by the official page or a public gazetteer. |
| `city_zh` | string | — | City in Chinese, as given on the official page. |
| `address_en` | string | — | Street address in English as published; blank when not published. |
| `lng` | number | degrees | Longitude, WGS-84 (EPSG:4326). Recorded only when published by the source; never inferred. Bounds: -180 to 180. |
| `lat` | number | degrees | Latitude, WGS-84. Recorded only when published by the source; never inferred. Bounds: -90 to 90. |
| `geo_precision` | enum | — | `venue` = property-level point; `city_only` = city known, coordinates withheld; `none` = no coordinates. |
| `website` | string | — | URL of the hotel's official page. |
| `updated_at` | date | — | Record update date, YYYY-MM-DD. |
| `license` | string | — | Data licence: `CC-BY-4.0`; credit EVENTTHING Venue Library. |
| `opening_year` | integer | year | Four-digit opening year as published; blank when not published. |
| `status` | enum | — | Operating status. One of `open`, `closed`, `renovating`, `under_construction`, `unknown`. See “Status model”. |
| `status_source` | enum | — | Evidence type behind `status`. See “Status model”. |
| `status_asof` | date | — | Date of the evidence behind `status`, YYYY-MM-DD. |

## 2. `venues.public.csv` — 17 columns

China venue master list — one row per venue. **3,549 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `master_id` | string | — | Unique venue ID (e.g. BJ001). Primary key. |
| `name_zh` | string | — | Chinese venue name as published. |
| `name_en` | string | — | English venue name where the source publishes one; blank otherwise (641 of 3,549 rows). |
| `category` | enum | — | Venue category: `商业` (commercial), `酒店` (hotel), `会展` (exhibition/convention), `体育` (sports), `特殊景点场地` (scenic/special site). |
| `sub_type` | string | — | Finer type as recorded, e.g. `商场` (mall), `商业地产场地` (commercial property), `酒店会议设施` (hotel meeting facilities), `展览中心`, `体育场`. |
| `country` | string | — | Country in Chinese. All rows in this release are `中国`. |
| `province` | string | — | Province or municipality in Chinese; blank when not recorded. |
| `city` | string | — | City in Chinese. |
| `district` | string | — | District in Chinese; blank when not recorded. |
| `address` | string | — | Street address in Chinese as published. |
| `source_url` | string | — | Public source page for the record. Commercial venues are blank by policy: third-party deep links are not redistributed. 421 of 3,549 rows carry a URL. |
| `lng` | number | degrees | WGS-84 longitude. Commercial venues are blank by policy. 656 of 3,549 rows carry a point. |
| `lat` | number | degrees | WGS-84 latitude; same policy as `lng`. |
| `status` | enum | — | Operating status: `open`, `closed`, `renovating`, `under_construction`, `unknown`. `unknown` means not verified — not closed. See “Status model”. |
| `status_source` | enum | — | Evidence type: `derived_from_hotels_asia`, `third_party_listing`, `official_site`, `retired_list`, `not_verified`, `no_source_link`. See “Status model”. |
| `status_asof` | date | — | Date of the evidence, YYYY-MM-DD. |
| `hotel_id_ref` | string | — | For the 441 venues that also appear in hotels.public.csv, the hotel `id` that points here; empty otherwise. Lets readers reproduce the de-duplication behind the 6,146 headline. |

## 3. `cases.csv` — 14 columns

Case index — one row per case; links only, no body text. **1,309 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `case_id` | string | — | Stable ID derived from the original URL; unique within the file. |
| `venue_id` | string | — | Joins to `venues.public.csv.master_id` where the venue is published; blank when the case is not tied to a venue. A few rows reference venues not yet in the public directory. |
| `venue_name` | string | — | Venue name in Chinese, as published on the source page. |
| `venue_name_en` | string | — | Venue name in English where the source gives one; blank otherwise. |
| `city` | string | — | City in Chinese. |
| `city_en` | string | — | City in English where the source gives one. |
| `brand` | string | — | Brand credited for the case, as published (bilingual where the source gives both). |
| `brand_en` | string | — | English brand name where the source gives one. |
| `year` | integer | year | Four-digit year the case ran, as published. |
| `title` | string | — | Case title in the language of the source (`lang`). No body text is included. |
| `lang` | enum | — | Language of `title`. |
| `source` | string | — | Publisher name: OnsiteClub or a media outlet. This is not a URL — the link is in `url`. |
| `published_at` | date | — | Publication date, YYYY-MM-DD, when derivable from the URL; blank otherwise. |
| `url` | string | — | Link to the original; no body text. |

## 4. `sample-80-halls-20261027.csv` — 21 columns

80-hotel hall sample — one row per meeting room / hall. **2,100 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `venue_id` | string | — | Hotel ID this hall belongs to (SHL-* / MAR-*); joins `sample-80-venues-20261027.csv`. |
| `venue_name` | string | — | Hotel name as recorded in the source. |
| `city` | string | — | City of the hotel. |
| `country` | string | — | Country of the hotel (English). |
| `room_id` | string | — | Unique hall / meeting-space ID. Primary key. |
| `room_name` | string | — | Hall name as published (Chinese or English as in the source). |
| `area_sqm` | number | m² | **Published area** of the hall in m². Usually the net exhibition area; for multi-storey halls, the sum of the floors. Blank when not published; never computed from length × width. |
| `length_m` | number | m | Length in metres of the hall's **building outline** (wall to wall), which includes walls, columns, plant rooms and circulation; blank when not published; never used to derive `area_sqm`. |
| `width_m` | number | m | Width in metres of the hall's **building outline**; same rule as `length_m`. |
| `height_m` | number | m | Ceiling height in metres; blank when not published. |
| `capacity_banquet_pax` | integer | persons | Banquet (round-table) capacity as published. |
| `capacity_theater_pax` | integer | persons | Theatre-style capacity as published. |
| `capacity_classroom_pax` | integer | persons | Classroom-style capacity as published. |
| `capacity_reception_pax` | integer | persons | Standing reception capacity as published. |
| `capacity_max_pax` | integer | persons | Maximum capacity where the source gives only one number without a layout; not additive with the four layout capacities. |
| `source_url` | string | — | Source page for this hotel's hall data; every row carries one. |
| `data_level` | enum | — | `official` = parsed from the official site. Records flagged `suspect` are excluded from this sample. |
| `dims_qa` | string | — | Dimension QA note. Set when published area and length × width differ by more than 15%, so the two numbers are kept side by side. This is a caliber difference, not an error: the area is the published hall area (net exhibition area, or the sum of floors), while length × width is the building outline including walls, columns, plant rooms and circulation. Figures are never adjusted. |
| `status` | enum | — | Status of the hotel the hall belongs to (`open` for every row in this sample). See “Status model”. |
| `status_asof` | date | — | Date of the status evidence, YYYY-MM-DD. |
| `updated_at` | date | — | Record update date, YYYY-MM-DD. |

## 5. `sample-80-venues-20261027.csv` — 15 columns

The 60 sample hotels — one row per hotel. **80 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `venue_id` | string | — | Hotel ID (SHL-* / MAR-*); matches `venue_id` in the hall sample. Primary key. |
| `name_zh` | string | — | Chinese hotel name. |
| `name_en` | string | — | English hotel name; blank where the source has none (20 of 60 rows). |
| `city` | string | — | City (mixed Chinese/English as recorded). |
| `country` | string | — | Country in English. |
| `address` | string | — | Address as published. |
| `website` | string | — | Official hotel page. |
| `star_rating` | integer | stars | 4 or 5. |
| `brand_group` | string | — | Shangri-La or Marriott in this sample. |
| `brand` | string | — | Brand within the group. |
| `opening_year` | integer | year | Opening year; blank in all 60 sample rows (the sample does not carry it). |
| `lng` | number | degrees | WGS-84 longitude; blank when not published. |
| `lat` | number | degrees | WGS-84 latitude. |
| `updated_at` | date | — | Record update date, YYYY-MM-DD. |
| `license` | string | — | Data licence: `CC-BY-4.0`. |

## 6. `whitelist-v2.csv` — 4 columns

Release metadata — which source columns are published, which are withheld, and why. One row per source column. **113 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `file` | string | — | Source table the rule applies to: an internal master name (`hotels-asia.csv`, `venues.csv`) or a public batch file name. |
| `column` | string | — | Source column name the rule applies to. |
| `action` | enum | — | `keep` = published in the public file; `strip` = withheld. |
| `note` | string | — | Why the column is kept or withheld (internal editorial note, published for transparency). |

## 7. `batch2-exhibition-centres-20261029.csv` — 13 columns

Batch 2 — exhibition centres and convention venues across Asia; one row per venue. **104 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `venue_id` | string | — | Public venue ID (`expo-*`). Primary key. |
| `name_zh` | string | — | Venue name in Chinese, as published. |
| `country` | string | — | Country or territory in Chinese, as recorded in the source. |
| `city` | string | — | City in Chinese. |
| `address` | string | — | Street address as published; blank when the source publishes none (6 of 104 rows). |
| `website` | string | — | Official site or contact page; blank when not published (14 of 104 rows). |
| `halls_count` | integer | halls | Number of halls recorded for this venue in the hall file; 0 means no hall record was captured. |
| `halls_area_sqm` | number | m² | Sum of the areas recorded for this venue's halls, in square metres; blank when no hall area is published. Not the venue's published total exhibition area. |
| `status` | enum | — | `open` / `closed` / `renovating` / `under_construction` / `unknown`; see the status model in `fields.md`. |
| `status_note` | string | — | Short note behind `status`, in Chinese; published as recorded. |
| `intro_zh` | string | — | Chinese profile text; blank when the source has no usable text (63 of 104 rows). |
| `intro_en` | string | — | English profile text written from the source, not machine-translated; blank when none. |
| `source` | string | — | Where the profile came from (publisher and page type). |

## 8. `batch2-exhibition-halls-20261029.csv` — 13 columns

Batch 2 — hall-level records for the exhibition centres; one row per hall. **797 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `hall_uid` | string | — | Composite ID `venue_id:hall_id`, unique across the file. Primary key. |
| `venue_id` | string | — | Venue ID; joins to `batch2-exhibition-centres-20261029.csv`. |
| `venue_name` | string | — | Venue name copied from the venue record. |
| `hall_id` | string | — | Hall code as published; unique only within a venue. |
| `hall_name` | string | — | Hall name as published. |
| `area_sqm` | number | m² | Published hall area in square metres; blank when not published (165 of 797 rows). |
| `length_m` | number | m | Published hall length in metres; blank when not published. |
| `width_m` | number | m | Published hall width in metres; blank when not published. |
| `height_m` | number | m | Published ceiling height in metres; blank when not published. |
| `floor_load_t_sqm` | number | t/m² | Published floor load in tonnes per square metre; blank when not published. |
| `pillar_free` | string | — | Column-free status as published (`是`, `否`, `无柱`, `Y`); blank when not stated (605 of 797 rows). |
| `source_url` | string | — | Page the hall record came from. |
| `note` | string | — | Editorial note on the record; blank when none. |

## 9. `batch3-sports-arts-retail-popup-racing-20261029.csv` — 15 columns

Batch 3 — sports venues, arts venues, retail and pop-up spaces, and racing circuits; one row per venue. **559 rows.**

| Field | Type | Unit | Description |
|---|---|---|---|
| `group` | enum | — | Batch group: `sports` / `arts` / `retail` / `popup` / `racing`. |
| `venue_id` | string | — | Public venue ID. Primary key. |
| `name_zh` | string | — | Venue name in Chinese, as published. |
| `city` | string | — | City in Chinese; blank on 1 row where the source gives none. |
| `country` | string | — | Country or territory in Chinese, as recorded in the source. |
| `address` | string | — | Street address as published; blank when the source publishes none (3 of 559 rows). |
| `website` | string | — | Official site or contact page; blank when not published (68 of 559 rows). |
| `area_text` | string | — | Area as published, free text with the source's own unit (e.g. `建筑面积 120,000㎡`, `赛道 5.451 km / 16 弯`); blank when not published. |
| `capacity_text` | string | — | Capacity, grade or case count as published, free text (e.g. seats, FIA grade, pop-up case count); blank when not published. |
| `open_year` | string | — | Opening year as published; may carry a parenthetical note (e.g. `2019（2019年8月开馆）`); blank when not published. |
| `status` | enum | — | `open` / `closed` / `renovating` / `under_construction` / `unknown`; see the status model in `fields.md`. |
| `status_note` | string | — | Short note behind `status`, in Chinese; blank on most rows (537 of 559). |
| `intro_zh` | string | — | Chinese profile text; blank when the source has no usable text (70 of 559 rows). |
| `intro_en` | string | — | English profile text written from the source, not machine-translated; blank when none (70 of 559 rows). |
| `source` | string | — | Where the profile came from (publisher and page type); blank when none (70 of 559 rows). |

## Notes and conventions

- **Scope.** `hotels.public.csv` is the 4–5 star public layer (3,038 rows). The internal master also holds 1,246 three-star records as denominator data; they are not published. `venues.public.csv` is the full China venue list (3,549 rows), not a selection.
- **Commercial-venue policy.** For `category=商业`, `lng`, `lat` and `source_url` are blank for the whole class. This is a contractual restriction, not missing data.
- **Sample files.** Rooms carry length/width/height only where the official site publishes them. 39 rows carry a dimension-QA note (`dims_qa`) because area and length×width use different calibers; their length/width/height are now published as recorded. 3 `suspect` rows were removed. 1,039 of 2,100 halls have complete length/width/height.
- **Licence.** Data CC BY 4.0; code MIT. Credit “EVENTTHING Venue Library”.

*EVENTTHING · Hong Kong · venue.eventthing.ai*
