# VERIFIERS (Python)

This file is a reference for common verifier commands. Configure actual commands in `rlm/state.json`.

## Tests
- `python -m pytest -q`

## Lint (ruff)
- `python -m ruff check .`
- auto-fix: `python -m ruff check . --fix`

## Typecheck (mypy)
- `python -m mypy .`

## Format (optional)
- `python -m ruff format .`

If you don't use a tool, set its command to an empty string in `rlm/state.json`.
