---
name: code-quality-and-contract-audit
description: Use this skill at the start and before completing any code development or fixes to ensure full type annotations, regression tests, documentation, and changelog compliance.
---
- At start, verify all public functions have complete type annotations on parameters and return values; if missing, add them.
- Create or update regression tests in tests/test_regressions.py with one test function per fixed bug; ensure tests pass.
- Add or update CHANGELOG.md under '## Unreleased' with bullet points for each fix, including function names and short descriptions.
- Confirm all public functions have docstrings describing behavior and parameters.
- Ensure test modules and packages have valid Python names for import.
- Add or update pytest.ini to include the source directory in pythonpath if tests fail to import modules.
- Before completion, rerun all tests and confirm zero failures.
- If any audit step fails, fix the issue by adding missing annotations, tests, changelog entries, or configuration files.
