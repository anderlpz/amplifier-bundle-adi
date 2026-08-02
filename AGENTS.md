# AGENTS.md — Guidance for AI Agents Working in This Repo

This repository is **amplifier-bundle-adi** (namespace `adi`): the Amplifier
Design Intelligence bundle. If you are an AI agent modifying this repo, read this
first — it encodes invariants that are easy to break silently and that have
already cost real debugging time.

## What this bundle is

ADI runs a two-tier **certified convergence loop** on a rendered design target:

- **Tier 1 — Impeccable** (`modules/tool-impeccable`): deterministic slop
  detection. Returns `CLEAN` or `FINDINGS`.
- **Tier 2 — Design Intelligence Council** (official
  `microsoft/amplifier-bundle-design-council`, seven orthogonal lens skills):
  semantic evaluation.
- **quality-gate** (`agents/quality-gate.md`): the independent authority that
  certifies both tiers passed on the *same* render.

The user entry point is the `/adi <target>` slash command
(`skills/adi/SKILL.md`), which delegates to `agents/adi-orchestrator.md`. The
orchestrator is a **context sink**: all heavy composition (browser-tester,
design-council skills, tools) lives in its frontmatter and loads only when it is
spawned.

## Invariants — do not break these

1. **`/adi` is a skill front door, not a mode.** It takes a target argument and
   delegates. Keep `user-invocable: true` and `disable-model-invocation: true`
   in `skills/adi/SKILL.md`.

2. **`config.skills` must use a RESOLVABLE source form.** The mount-time resolver
   only handles `git+`/`https` URLs and literal filesystem paths. The
   `@namespace:path` **mention form is silently dropped** — skills vanish with no
   error and `/adi` stops registering. This exact bug cost days. Always use the
   `git+…#subdirectory=skills` form (see `behaviors/adi.yaml` and the
   orchestrator's `tool-skills` wiring). `tests/test_bundle_validation.py` fails
   loudly if an `@mention` form appears.

3. **quality-gate must stay independent and honest.** It never authors the work
   it judges, and it must never fabricate certification. If evidence that BOTH
   tiers passed on the SAME render is missing/mismatched, it returns
   `NOT CERTIFIED — <what's missing>`. Do not weaken the Honest-Stopping section.

4. **The orchestrator owns the convergence control flow.** Tier 1 strictly before
   Tier 2; re-run Tier 1 after any Tier 2 fix; hard-escalate after 5 iterations.
   There is no external recipe — do not re-introduce a placeholder recipe or a
   dead pointer to one.

5. **Tier 2 is the official design-council.** Do not reintroduce
   `design-intelligence-enhanced` or any personal fork as the Tier-2 evaluator.

## Verify after any change

- **Run the validation test:** `python -m pytest tests/test_bundle_validation.py`
  (or `python tests/test_bundle_validation.py`). It uses only stdlib + pyyaml.
- **Confirm `/adi` registers** in a fresh session after any skill/behavior change.
  Registration is the real symptom — verify it directly, not a proxy.
- **Module tests** if you touched `modules/`:
  `python -m pytest modules/tool-impeccable/tests modules/tool-dom-extract/tests`.

## Tool invocation contracts (keep consistent across three places)

`tool-impeccable` invokes the **global `impeccable` binary** (not `npx`). The
orchestrator preflight checks `which impeccable`, and the README says
`npm install -g impeccable`. If you change one, change all three.
`tool-dom-extract` invokes `agent-browser`; preflight and README must agree
likewise.
