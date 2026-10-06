---
name: parse-and-aggregate-structured-logs
description: Use when extracting error entries from logs to produce a normalized JSON summary with counts and timestamps.
---
- Filter log entries by severity level (e.g., ERROR or CRITICAL), ignoring case.
- Normalize timestamps to UTC in ISO 8601 format with 'Z' suffix.
- Normalize service names to lowercase with hyphens replaced by underscores.
- Extract main message and last line of exception traceback if present.
- Detect and sum repeated message counts from repeat indicators.
- Sort errors by service name and timestamp ascending.
- Aggregate counts by service for summary statistics.
- Include required metadata fields like schema version and generator name.
