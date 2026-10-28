# The complete 80-hotel sample (public example) · 2026-10-27

80 hotels / **2,100 meeting halls**, with a source on every row. The four groups differ in depth on purpose.

| Group | Hotels | Halls | Full length/width/height | Note |
|---|---:|---:|---:|---|
| Shangri-La | 20 | 503 | **477** | The official site gives length × width, area and ceiling height hall by hall — every field |
| Marriott (overseas) | 20 | 601 | **562** | The events pages give length, width, height and four layout capacities |
| Marriott China (area + max capacity) | 20 | 511 | **0** | The site publishes only area and maximum capacity — we take what it gives, no back-calculation |
| Hilton China (area + seven layouts) | 20 | 485 | **0** | The site publishes area and layout capacities but no dimensions — again, no back-calculation |
| **Total** | **80** | **2,100** | **1,039** | |

The Marriott China and Hilton groups exist as a statement: **where length, width and height are missing, it is not a collection gap — the venue does not publish them.**

## Fields (21 columns)

`venue_id, venue_name, city, country, room_id, room_name, area_sqm, length_m, width_m, height_m, capacity_banquet_pax, capacity_theater_pax, capacity_classroom_pax, capacity_reception_pax, capacity_max_pax, source_url, data_level, dims_qa, status, status_asof, updated_at`

## Quality rules (already applied)

- **3 rows removed** with `data_level=suspect` (MAR-SINSI-R029 / MAR-KULXR-R016 / MAR-KULPG-R002): area and capacity density clearly wrong;
- **39 rows** where area and length × width differ by more than 15%: the area is kept and the dimensions are recorded as published, flagged `dims_qa=area_dims_conflict`. **This is a normal difference of definition** (the area is the published hall area — usually net exhibition area, or the sum of floors for multi-level halls; length × width is the building outline, including walls, columns, plant rooms and circulation), not an error; see "Area and dimensions" in the main README;
- Those 39 rows carry their dimensions again in this edition (rows with complete length/width/height: 1,005 → **1,039**); we still never extrapolate, and never compute area from length × width;
- Non-numeric layout capacities (`-`, `28-30 tables`) → **384 cells blanked**; no conversion, no guessing;
- Hilton group: the source gives only area plus seven layouts (banquet / theatre / classroom(school) / reception / u-shape / conference / square), **no dimensions** → three columns blank, `dims_qa=source_no_dims` (a separate flag: not a conflict, simply not published). The public columns keep the first four plus `capacity_max_pax` (the largest of the seven); u-shape / conference / square stay internal;
- Hilton group: **17 rows** under 10 sqm removed (7–9 sqm meeting rooms, not ballrooms);
- `status=open`; `status_asof` is the crawl date for that group (Shangri-La/Marriott 2026-10-26, Hilton 2026-10-25), based on the brand's live booking/events pages, not verified on site;
- English names preferred; a missing English name is left blank (no machine translation);
- Encoding UTF-8 without BOM, LF; value-level PII has been cleared.
- **Only `status` and `status_asof`, no `status_source`** (the three columns are intentionally incomplete here: this is a display sample; the two main files are the data files). The evidence is the same as the main tables — the brand's live booking pages.

## How to use

```python
import pandas as pd
halls = pd.read_csv('sample-80-halls-20261027.csv')
# Example: halls in Shanghai, 1,000 sqm or more, ceiling height 6 m or more
print(halls[halls.city.isin(['上海', 'Shanghai']) & (halls.area_sqm >= 1000) & (halls.height_m >= 6)]
      [['venue_name', 'room_name', 'area_sqm', 'length_m', 'width_m', 'height_m']])
```

> If you only want rows with dimensions: `halls[halls.height_m.notna()]` (the Shanghai filter above already implies it in this example).

**Licence**: data CC BY 4.0; please credit the source when citing (see `CITATION.cff` in the repository root).

—— EVENTTHING
