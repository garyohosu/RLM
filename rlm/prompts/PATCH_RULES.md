# PATCH RULES (Min-diff discipline)

## Hard constraints
- No large refactors unless the user requests them.
- Prefer editing existing functions over creating new architecture.
- Keep each iteration small:
  - ≤ 100 lines changed total unless necessary
  - ≤ 3 files touched unless necessary

## When adding code
- Add/adjust tests first if behavior is unclear.
- Add docstrings only when they clarify intent for verifiers.
- Avoid cleverness. Prefer simple, readable code.

## When fixing tests
- Do not weaken assertions to "make it pass".
- If a test is wrong, explain why and replace it with a better one.

## Commit-style messaging (optional)
At the end of each iteration, produce:
- "Patch intent:"
- "Files changed:"
- "Why it fixes the failure:"
