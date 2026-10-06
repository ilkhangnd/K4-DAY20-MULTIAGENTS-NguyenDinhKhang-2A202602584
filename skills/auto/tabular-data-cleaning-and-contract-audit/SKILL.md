---
name: tabular-data-cleaning-and-contract-audit
description: Use this skill at the start and before completing any tabular data processing task to normalize, clean, and produce contract-compliant CSV and JSON outputs.
---
- At start, read input CSV and data dictionary to understand columns and formats.
- Normalize all categorical fields to canonical spelling and capitalization (e.g., region names).
- Parse all date/time fields into consistent UTC ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
- Remove duplicate rows based on unique keys (e.g., order_id), counting duplicates removed.
- Convert all monetary values to integer cents (multiply by 100 and convert to int).
- Exclude or mark rows with missing or invalid values as specified (e.g., amount = -999).
- Write cleaned CSV to workspace/clean.csv with exact header order and required columns.
- Create or update answer.json with required metrics and a meta object containing:
  - source: input filename
  - rows_in: total input rows including duplicates
  - rows_used: distinct rows with known amounts
- Before completion, audit output schema, metadata presence, normalized values, and companion files; create or fix any missing or incorrect items.
