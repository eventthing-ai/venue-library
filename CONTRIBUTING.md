# Contributing to the EVENTTHING Venue Library

This repository is a **public reference layer** for venue data. Corrections, new venues and
additional countries are welcome. Every contribution goes through the same gate — a pull request
that fails validation is not merged.

---

## 1. What we accept

| Kind of contribution | How it works |
|---|---|
| **Correction** (wrong name, address, category, coordinates, status) | Open an issue with the file, the record ID, the current value, the correct value and a **public source URL** |
| **New venue** | Open an issue first; for a single record, add a row to `data/venues.public.csv` following `schema/venues.public.schema.json` and run `python3 validate.py` |
| **New country / city batch** | Open an issue first — we agree on scope and field coverage before a bulk PR |
| **Tooling** (loaders, validators, converters) | PR against `scripts/`; must not add runtime dependencies without discussion |

Hotel records in `data/hotels.public.csv` are a projection of a maintained inventory. Please send
corrections as an issue rather than editing that file directly; we will fix the source and rebuild
the projection, so the row count and SHA-256 stay reproducible.

## 2. What we do not accept

- **Data without a public source.** A correction must point to an official venue page, a national
  venue/convention association listing, a municipal government page, or a comparable public record.
  “I know this venue” is not a source.
- **Personal contact data.** Named individuals, personal mobile numbers and personal email
  addresses are removed on sight. The public layer contains none, and PRs must not add any.
- **Coordinates without a datum.** See rule 3 below.
- **Scraped bulk dumps** from directories whose terms forbid redistribution.
- **Machine-translated venue names.** If the venue publishes no official Chinese (or English)
  name, the field stays empty.

## 3. Coordinate rules (the one thing most contributions get wrong)

1. **WGS-84 only.** If your source is Amap/Gaode/Tencent, the point is GCJ-02; if it is Baidu, it is
   BD-09. Convert before submitting.
2. **State the source** in the issue: the venue page, the map widget, or the public record you used.
3. **Never interpolate, never pad.** No point is better than a point in the middle of the city.
   Leave `lng`/`lat` empty.
4. **Respect the policy.** Commercial-category venue coordinates are withheld in the public file.
   Do not add them through a PR.

Full explanation: [`docs/coordinates.md`](docs/coordinates.md).

## 4. Field conventions

- `fields.md` is the dictionary — every column, its unit and its convention, in English, Chinese and French.
- Empty string and `null` mean the same thing: **not published**. `0` is a value, blank is not.
- Numbers are stored as plain digits (no units, no thousands separators). Units live in the column name or in `fields.md`.
- Hotels: `id` and `slug` are unique. Venues: `master_id` is unique. Sample files: `venue_id` groups rows, `room_id` is unique within the hall sample.
- Dates are `YYYY-MM-DD`.
- `status` is one of `open`, `closed`, `unknown`; `status_source` names the evidence type. Do not
  mark a record `open` without a source, and do not treat `unknown` as open.

## 5. Before you open the PR

If you changed a CSV, regenerate the derived files first:

```bash
python3 scripts/gen_schema.py            # rewrite schema/ and schema/_index.json
python3 scripts/gen_fields_md.py         # rewrite fields.md
python3 scripts/build_coverage.py        # rewrite quality/coverage.md
python3 validate.py                      # structural and semantic checks
```

All four must pass, and the regenerated files belong in the same PR. Review runs the read-only
variants (`gen_schema.py --check`, `gen_fields_md.py --check`, `build_coverage.py --check`) to
confirm the committed files are current. There is no hidden CI step beyond these checks.

## 6. Review

- One reviewer, one working day.
- Corrections with a public source are fast-tracked; new venue batches are reviewed in bulk.
- We may decline data that is accurate but not redistributable.

## 7. Licence of your contribution

By contributing you agree that data is published under **CC BY 4.0** and code under **MIT**, and
that you have the right to license it that way. Do not paste content from a source that forbids
redistribution (e.g. Wikipedia text is CC BY-SA — facts are fine, prose is not).

*EVENTTHING · Hong Kong · venue.eventthing.ai*
