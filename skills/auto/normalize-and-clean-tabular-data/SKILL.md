---
name: normalize-and-clean-tabular-data
description: Use when processing CSV or tabular data to standardize formats, handle missing values, and remove duplicates.
---
- Normalize categorical fields (e.g., region names) by trimming whitespace and applying canonical casing.
- Parse date/time fields from multiple formats and convert all to a single timezone-aware UTC format.
- Convert monetary values to integer cents, treating sentinel values (e.g., -999) as missing.
- Remove duplicate rows based on all relevant columns.
- Write cleaned data to output with correct headers and formats.
