<!-- Thanks for contributing to ADI. Keep PRs focused and fill in the checklist. -->

## What & why

<!-- One or two sentences: what does this change do, and why? -->

## Checklist

- [ ] **Bundle composes** — loads without errors.
- [ ] **`/adi` registers** as a slash command in a fresh session (verified directly, not a proxy). Required for any skill/behavior/manifest change.
- [ ] **Validation test passes** — `python -m pytest tests/test_bundle_validation.py` (or `python tests/test_bundle_validation.py`).
- [ ] **Module tests pass** (if `modules/` touched) — `python -m pytest modules/tool-impeccable/tests modules/tool-dom-extract/tests`.
- [ ] **Skill wiring uses a resolvable source** (`git+`/`https`/local path) — never the `@mention` form in `config.skills`.
- [ ] **Invariants intact** (see `AGENTS.md`) — quality-gate stays independent/honest; orchestrator owns the loop; Tier 2 is the official design-council.
- [ ] **Docs updated** — `README.md` reflects any behavior change.

## Notes

<!-- Anything reviewers should know: trade-offs, follow-ups, things you couldn't verify. -->
