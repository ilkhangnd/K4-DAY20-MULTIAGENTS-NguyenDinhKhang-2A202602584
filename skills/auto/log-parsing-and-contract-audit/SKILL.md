---
name: log-parsing-and-contract-audit
description: Use this skill at the start and before completing any log analysis task to parse, normalize, and produce contract-compliant JSON error reports.
---
- At start, read raw log file and identify entries with level ERROR or CRITICAL (case insensitive).
- Normalize timestamps to UTC in ISO 8601 format with 'Z' suffix (YYYY-MM-DDTHH:MM:SSZ).
- Normalize service names to lower-case with hyphens replaced by underscores.
- Extract message text after the service name on the first line.
- Extract the last line of any traceback as the exception field; use null if none.
- Calculate repeat_count as 1 plus all counts from subsequent "-- last message repeated N times --" lines.
- Sort errors by service name, then by timestamp ascending.
- Aggregate counts_by_service summing repeat_count per service.
- Create or update output JSON with top-level keys: schema_version=2, generated_by="log-triage", errors array, and counts_by_service object.
- Before completion, audit JSON schema, metadata, normalized fields, ordering, and aggregate counts; create or fix any missing or incorrect items.
