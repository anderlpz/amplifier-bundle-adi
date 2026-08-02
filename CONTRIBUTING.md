# Contributing to ADI

Thanks for your interest in **Amplifier Design Intelligence (ADI)**.

## Contribution stance

This is a personal MIT-licensed bundle maintained by [@anderlpz](https://github.com/anderlpz).
Large external code contributions are not actively solicited, but **issues are
welcome** — bug reports, install problems, and suggestions all help make ADI a
better exemplar. If in doubt, open an issue before a PR.

## Before you open a PR

ADI is an Amplifier bundle. Its correctness depends on a few invariants that are
easy to break silently (see [`AGENTS.md`](AGENTS.md) for the full list). At
minimum, verify:

1. **The bundle composes and `/adi` registers.** After any change to skills,
   behaviors, or the bundle manifest, confirm `/adi` still appears as a slash
   command in a fresh session.
2. **The validation test passes:**
   ```bash
   python -m pytest tests/test_bundle_validation.py
   # or, with no pytest:
   python tests/test_bundle_validation.py
   ```
3. **Module tests pass** (if you touched `modules/`):
   ```bash
   python -m pytest modules/tool-impeccable/tests modules/tool-dom-extract/tests
   ```
4. **Docs updated** — if behavior changed, update `README.md` accordingly.

## Skill wiring — the one thing that keeps biting

`config.skills` in `behaviors/adi.yaml` (and in the orchestrator's `tool-skills`
wiring) MUST use a resolvable source form — a `git+`/`https` URL or an existing
local path. The `@namespace:path` mention form is **silently dropped** by the
mount-time resolver, which makes skills invisible with no error. The validation
test fails loudly if an `@mention` form sneaks in. Don't work around it.

## License

By contributing, you agree that your contributions are licensed under the
project's [MIT License](LICENSE).
