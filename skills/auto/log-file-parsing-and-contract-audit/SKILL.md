---
name: log-file-parsing-and-contract-audit
description: Use this at the start and before completing any log processing task to parse, normalize, and audit logs for schema, metadata, ordering, and counts.
---
- At start: Read raw log lines and parse timestamps, converting all to UTC in YYYY-MM-DDTHH:MM:SSZ format.
- At start: Normalize service names to lower-case with '-' replaced by '_'.
- At start: Extract level in upper case.
- At start: Extract message as text after '<service>: ' on first line.
- At start: Extract exception as last line of traceback or null if none.
- At start: Calculate repeat_count as 1 plus sum of N from subsequent '-- last message repeated N times --' lines.
- Before completion: Sort errors by service, then timestamp_utc ascending.
- Before completion: Aggregate counts by service summing repeat_count.
- Before completion: Create or update output JSON with top-level keys "schema_version": 2 and "generated_by": "log-triage".
- Before completion: Fix any missing or malformed fields, ordering, or counts.
