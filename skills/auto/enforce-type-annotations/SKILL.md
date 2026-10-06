---
name: enforce-type-annotations
description: Use when writing or reviewing public functions to ensure all parameters and return types have type hints.
---
- Identify all public functions in the module (names not starting with '_').
- Add explicit type annotations for every parameter and the return value.
- Verify annotations are syntactically correct and consistent with usage.
- Run static type checks if available to confirm coverage.
