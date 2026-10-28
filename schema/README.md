# Schema

Machine-readable descriptions of every CSV in `data/`. Generated from the files that actually ship in
the public repository by `scripts/gen_schema.py`, so the schema cannot drift from the data.
`python3 scripts/gen_schema.py --check` exits non-zero when it does.

| File | Schema | Rows | Columns |
|---|---|---:|---:|
| `data/hotels.public.csv` | [`hotels.public.schema.json`](hotels.public.schema.json) | 3,038 | 23 |
| `data/venues.public.csv` | [`venues.public.schema.json`](venues.public.schema.json) | 3,549 | 17 |
| `data/sample-80-halls-20261027.csv` | [`sample-80-halls.schema.json`](sample-80-halls.schema.json) | 2,100 | 21 |
| `data/sample-80-venues-20261027.csv` | [`sample-80-venues.schema.json`](sample-80-venues.schema.json) | 60 | 15 |
| `data/whitelist-v2.csv` | [`whitelist-v2.schema.json`](whitelist-v2.schema.json) | 72 | 4 |

`_index.json` carries the authoritative row counts, column counts and SHA-256 of the file each
schema was generated from. Read it first if you need to know what you are looking at.

## How to use a schema

```python
import csv, json, jsonschema

schema = json.load(open("schema/hotels.public.schema.json"))
with open("data/hotels.public.csv", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

errors = 0
for i, row in enumerate(rows, 2):
    # CSV gives strings; number-typed fields must be coerced before validation
    record = {k: (v if v != "" else None) for k, v in row.items()}
    for k, prop in schema["properties"].items():
        if ({"number", "integer"} & set(prop.get("type", []))) and record.get(k) is not None:
            try:
                record[k] = float(record[k]) if "number" in prop["type"] else int(float(record[k]))
            except (TypeError, ValueError):
                errors += 1
    for err in jsonschema.Draft202012Validator(schema).iter_errors(record):
        errors += 1
        if errors < 10:
            print(f"row {i}: {err.json_path}: {err.message}")
print("rows", len(rows), "errors", errors)
```

## Conventions the schemas encode

- **Empty means unpublished.** Every field is `["string", "null"]` unless it is numeric; an empty
  CSV cell is `null`, never `0` and never `"N/A"`.
- **Numbers are numbers.** Numeric columns are typed `number` (decimals, e.g. coordinates) or
  `integer` (counts, years, capacities) and must parse as such (no units, no thousands separators).
- **Small vocabularies are enums, declared explicitly.** Only genuinely categorical columns get an
  enum (`category`, `status`, `status_source`, `geo_precision`, …). Dates and free text never do,
  even when the current file happens to contain few distinct values.
- **Dates are ISO.** `*_at` and `*_asof` columns carry `format: date` and a `YYYY-MM-DD` pattern.
- **Coordinates are WGS-84** and bounded by `minimum`/`maximum`. See [`../docs/coordinates.md`](../docs/coordinates.md).
- `additionalProperties: false` — an unexpected column is a schema violation, not a bonus.

## Regenerating

```bash
python3 scripts/gen_schema.py           # rewrite schema/
python3 scripts/gen_schema.py --check   # exit 1 if stale
python3 scripts/gen_fields_md.py        # rewrite fields.md
python3 scripts/gen_fields_md.py --check
python3 scripts/build_coverage.py       # rewrite quality/coverage.md
python3 scripts/build_coverage.py --check
python3 validate.py                     # check every CSV against its schema
```

*EVENTTHING · Hong Kong · venue.eventthing.ai*
