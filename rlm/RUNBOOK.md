# RUNBOOK: Generic RLM loop (Python) for Claude Code

This runbook is written to be followed inside Claude Code.

## Directory convention
- `workspace/` is the target project area (code, tests, configs).
- `rlm/` contains the loop state and prompt templates.

If you already have a standard Python repo layout, you may ignore `workspace/` and treat your repo root as the "workspace".
In that case update `rlm/state.json` paths accordingly.

---

## Step 0 — Choose your verifier commands

Edit `rlm/state.json` and set:

- `verifiers.commands.tests`   (default: `python -m pytest -q`)
- `verifiers.commands.lint`    (default: `python -m ruff check .`)
- `verifiers.commands.typecheck` (optional: `python -m mypy .`)

If you are not using ruff/mypy, set them to empty string.

---

## Step 1 — Write a spec and success criteria

Fill these fields in `rlm/state.json`:

- `goal.statement`
- `goal.success_criteria` (a checklist)
- `constraints` (what is forbidden / required)
- `scope` (what files may be changed)

**Important:** Do NOT relax success criteria during the loop. Fix the code instead.

---

## Step 2 — Orchestrate the first plan

In Claude Code, paste the contents of `rlm/prompts/ORCHESTRATOR.md` as a system-style instruction (or just as a message)
and then ask:

- "Create the initial plan and create/adjust files in workspace accordingly."

Claude should:
- produce a plan,
- propose minimal tasks,
- start executing (creating code/tests) inside `workspace/`.

---

## Step 3 — Run verifiers, capture logs, iterate

After Claude makes a change, run:

- tests:  (see rlm/state.json: verifiers.commands.tests)
- lint:   (see rlm/state.json: verifiers.commands.lint)
- types:  (see rlm/state.json: verifiers.commands.typecheck)

Paste the outputs back to Claude and ask it to:
- update `rlm/state.json` (or a `rlm/logs/latest.txt`) with the failing logs,
- propose the *minimum patch*,
- apply the patch as a small diff,
- re-run verifiers.

Use `rlm/prompts/CRITIC.md` whenever you want to force rigorous log-based diagnosis.

---

## Step 4 — Stop conditions

Stop the loop when:
- all enabled verifiers pass, AND
- all success criteria are met.

If the loop stalls:
- tighten the scope (change fewer files),
- reduce patch size (one failure at a time),
- add a focused test that reproduces the bug.

---

## Tip: Keep patches small

A healthy loop looks like:
- 1–3 files changed per iteration
- 1–2 root-cause fixes per iteration
- verifiers run every iteration

---

## Optional: Audit trail

- Store each verifier output in `rlm/logs/iter_XX.txt`
- Keep `rlm/state.json` updated each iteration

This makes the loop reproducible and debuggable.
