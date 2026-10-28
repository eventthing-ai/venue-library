# Coordinates in this dataset

*How every `lng` / `lat` pair in the public files was produced, and how far you should trust it.*


---

## 1. The rule

**Every coordinate in this repository is WGS-84** — the GPS datum used by OpenStreetMap, devices and most international APIs.

That sentence matters more than it looks. Chinese venue data circulates in three coordinate systems, each roughly **500 metres** away from the others:

| System | Who uses it | Offset vs WGS-84 |
|---|---|---|
| **WGS-84** | GPS, OpenStreetMap, international APIs | — (reference) |
| **GCJ-02** | Chinese mapping providers (Amap/Gaode, Tencent), most Chinese property and booking sites | ≈ +500 to +600 m, direction varies by region |
| **BD-09** | Baidu Maps; anything scraped from a Baidu-based page | GCJ-02 **plus** another ≈ +600 m |

A dataset that mixes these three silently is not “slightly off” — it puts venues on the wrong block, sometimes the wrong side of a river. Everything published here was converted to WGS-84 during collection.

## 2. What is published

The public CSVs carry coordinates as two plain numbers, `lng` and `lat`. Per-row provenance columns
(`coord_source`, `coord_grade`, `coord_check_m`) and the internal geocoding cache are retained
internally and are **not** part of the public layer.

Coverage in the public files:

| File | Rows with `lng`/`lat` | Coverage | Note |
|---|---:|---:|---|
| `hotels.public.csv` | 1,492 / 3,038 | 49.1% | only points published by the hotel or its group |
| `venues.public.csv` | 656 / 3,549 | 18.5% | commercial-category coordinates withheld by policy; non-commercial coverage is 656 / 698 = 94.0% |
| `sample-80-venues-20261027.csv` | 40 / 80 | 66.7% | sample file |

## 3. What a blank coordinate means

**No trustworthy point was found — so the cell is empty.** Nothing is interpolated, nothing is
replaced by a city centroid, and no coordinate is inferred from an address. A blank is information:
it tells you the record is a directory entry, not a mapped property.

Commercial-category venues are a deliberate case: their coordinates are withheld by policy even
where the internal record has a point. That is why `venues.public.csv` shows 18.5% coordinate
coverage while the non-commercial categories are almost fully covered.

## 4. How to use a point

Treat a published point as **the venue's block — good enough to route to the door and to compare
neighbours**. Do not treat it as a survey marker. For a site visit, confirm the entrance.

Conversion and spot-check notes are kept in the internal build record. The public promise is
narrower and testable: the datum is WGS-84, the point came from a published source, and a blank
means no such point.

---
