---
name: tabular-data-cleaning-and-contract-audit
description: Use this at the start and before completing any tabular data task to clean, normalize, and produce required output files with metadata and schema.
---
- At start: Load input CSV with proper parsing of dates and string trimming.
- At start: Normalize categorical fields to canonical spellings (e.g., capitalize region names).
- At start: Remove duplicate rows.
- At start: Identify and handle missing or sentinel values (e.g., amount == -999).
- Before completion: Write workspace/clean.csv with header order_id,timestamp_utc,region,amount_cents.
- Before completion: Format timestamp_utc as ISO 8601 UTC (YYYY-MM-DDTHH:MM:SSZ).
- Before completion: Convert amount to integer cents.
- Before completion: Ensure region uses canonical spelling (North, South, East, West).
- Before completion: Include one row per distinct order with known amount.
- Before completion: Create or update metadata block describing output schema and companion files if applicable.
- Before completion: Save output JSON answer files with quoted keys and valid JSON syntax.
