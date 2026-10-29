# Example: a booking request expressed against the venue library

This is a worked example for AI agents and integrators. It shows how a brand-side agent can describe an
event requirement using the same fields that the CSVs publish, and what a venue-side answer would need to
contain to be comparable.

**Everything in this example is fictional.** The event, the company, the venue shortlist and the numbers
are made up. There are no real contact details, no real email addresses and no real prices anywhere in
this file — by design. Business enquiries go through the contact form on https://eventthing.ai .

---

## 1. The request (brand-side agent)

```json
{
  "request_id": "example-2026-0001",
  "event": {
    "type": "product_launch",
    "purpose": "press conference + evening reception",
    "date_window": {"from": "2027-03-10", "to": "2027-03-12"},
    "duration_days": 2
  },
  "attendance": {
    "conference_max": 500,
    "banquet_max": 320,
    "standing_reception": 600
  },
  "space": {
    "min_total_sqm": 1200,
    "min_ceiling_m": 6.0,
    "needs_column_free": true,
    "needs_loading_access": true
  },
  "location": {
    "country": "CN",
    "city": "Shanghai",
    "max_distance_km_from_city_centre": 25
  },
  "facilities": {
    "meeting_rooms_min": 4,
    "av": ["led_wall", "line_array_audio"],
    "parking_bays_min": 80
  },
  "commercial": {
    "budget_band": "not disclosed in this example",
    "decision_deadline": "2027-01-15"
  }
}
```

## 2. How to query the data

Shortlist in this order — it keeps the candidate set small before you pay for detail:

1. `data/venues.public.csv` — filter `country = 中国` (China), `city = 上海` (Shanghai), then `category` / `sub_type`
   (`会展` exhibition, `酒店` hotel, `商业` commercial, `体育` sports, `特殊景点场地` special-attraction venue).
2. `data/hotels.public.csv` — filter `country`, `city`, `brand_group`, `star_rating`; match on `id` / `slug`.
   Hall-level fields (meeting rooms, largest space, capacities) are not in the open hotel CSV; they are
   served through the API.
3. `data/sample-80-venues-20261027.csv` and `data/sample-80-halls-20261027.csv` — the 80-hotel complete sample:
   room-level area, dimensions, ceiling height and layout capacities, with a `source_url` on every row.
   Use it to check field semantics before ordering the API.

Rules that matter:

- Match on `id` / `slug`, never on display name alone (the same venue can appear in more than one file).
- Treat empty as unknown, not as zero. If a hall-level field is absent from the open edition, the value is
  not published openly — do not infer.
- `area_sqm` and `capacity_*` are numbers in CSV text; parse before comparing.
- Coordinates are WGS-84; `geo_precision` tells you whether a point is the venue itself or a city-level
  approximation.

## 3. What a venue-side answer should look like

The point of the dataset is comparability, so an answer is only useful if it uses the same field names:

```json
{
  "request_id": "example-2026-0001",
  "venue_id": "EXAMPLE-VENUE-001",
  "available": true,
  "date_hold": {"from": "2027-03-10", "to": "2027-03-12", "status": "tentative"},
  "space_offered": [
    {"room": "Grand Hall", "area_sqm": 1380, "ceiling_m": 8.5, "banquet_max": 700, "theatre_max": 900},
    {"room": "Studio 3", "area_sqm": 210, "ceiling_m": 5.0, "theatre_max": 140}
  ],
  "included": ["basic lighting", "house sound", "two green rooms"],
  "not_included": ["rigging above 6 m", "freight lift after 22:00"],
  "next_step": "site visit",
  "note": "Fictional example. No price, no contact details, no commitment."
}
```

## 4. What this example deliberately does not contain

- No real venue names, no real people, no phone numbers, no email addresses.
- No prices or rate cards — those are a commercial conversation, not open data.
- No promise of availability. A dataset row means "this venue exists and publishes these fields",
  not "this venue is free on your date".

For a real enquiry, use https://eventthing.ai .
