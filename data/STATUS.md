# Status coverage · 2026-10-26 (public-layer definition)

**In one line: of the 3,549 China venues, 559 (16%) can be tied to a status source; the remaining 2,988 are marked unverified and are not counted as open.** (In the public file, 421 venues = 11.9% carry a `source_url`.)

## 1. Venues (venues.public.csv, 3,549 rows)

| status | status_source | Rows | What it means |
|---|---|---:|---|
| open | derived_from_hotels_asia | 441 | Back-filled through `venue_id_ref` from the hotel master table, whose evidence is the brand's live booking page |
| open | third_party_listing | 102 | Third-party listing pages (links withheld under policy; evidence kept internally) |
| open | official_site | 16 | The venue's own current website |
| closed | retired_list | 2 | Verified as closed |
| unknown | not_verified | 2,952 | Not verified |
| unknown | no_source_link | 36 | Previously marked open but with no link at all — downgraded |
| **Total** | | **3,549** | open 559 / closed 2 / unknown 2,988 |

## 2. Hotels (hotels.public.csv, 3,038 rows = 4–5 star)

- `status=open`, `status_source=official_site_listed`, `status_asof=2026-10-26`;
- The evidence is the brand's live booking page (Marriott / Hilton / Accor / Wyndham / Shangri-La / IHG); **not verified on site**;
- The 1,246 three-star records (Wyndham 697 + Hilton Garden Inn 549) stay internal as a denominator and are not published.

## 3. Three rules

1. **unknown = unverified** and is never counted as open; README and copy use "status where we hold a source".
2. We never claim "all open", and never turn unknown into open.
2b. **The 102 `third_party_listing` rows carry no link in the public file** (commercial sources are withheld as a class); the evidence stays internal, and the README states this so readers do not see an "open" row without support.
3. Every open row carries `status_source`; there are only four source types: `derived_from_hotels_asia / third_party_listing / official_site / official_site_listed`.

## 4. Re-verification plan (summary)

- The 2,988 unverified rows = `not_verified` 2,952 + `no_source_link` 36; the table below covers the **not_verified 2,952** (the other 36 are not listed).
- Priority: the top 12 cities (Shanghai 402 / Shenzhen 282 / Guangzhou 249 / Beijing 241 / Chengdu 139 / Wuhan 130 / Nanjing 117 / Hangzhou 109 / Suzhou 96 / Changsha 93 / Chongqing 92 / Xi'an 90);
- Two cities per week, completed within November; coverage is recalculated and this file updated after each batch.

—— EVENTTHING
