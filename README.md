# Amplifier Design Intelligence (ADI)

A two-tier convergence loop for design quality — Impeccable keeps the floor clean (deterministic slop detection on live DOM), the Design Intelligence Council focuses on the ceiling (7-lens semantic evaluation). Both must pass on the same render for the loop to exit.

## Installation

One command. `/adi` then works in every session — no need to switch your active
bundle. Same as `/design-council` and the other `/`-command bundles.

### Option 1 — Full bundle (recommended)

Self-contained: brings ADI plus its baseline dependencies. Best if you're not
sure which to pick.

```bash
amplifier bundle add git+https://github.com/anderlpz/amplifier-bundle-adi@main --app
```

### Option 2 — Behavior only (lightweight)

Just ADI's wiring (its agents + the `/adi` skill), with no baseline dependencies
pulled in — it slots into your existing setup. Ideal if you already run a loaded
rig with other `/`-command bundles (this is how `superpowers`, `team-pulse`, and
`design-council` behaviors are typically added):

```bash
amplifier bundle add "git+https://github.com/anderlpz/amplifier-bundle-adi@main#subdirectory=behaviors/adi.yaml" --app
```

Both options are verified end-to-end. Either way, start (or restart) a session
and `/adi` is available:

```
/adi https://staging.example.com/pricing
```

> **Why `--app`?** It adds ADI as an "app bundle" that's always composed in, so
> you never have to run `amplifier bundle use`. Leave off `--app` if you only
> want ADI registered for occasional use via `amplifier bundle use adi` instead.

Prefer to wire it into a bundle you already maintain? Include it in that bundle's
`bundle.md` — it composes cleanly next to design-council and other `/`-command
bundles:

```yaml
includes:
  # full bundle
  - bundle: git+https://github.com/anderlpz/amplifier-bundle-adi@main
  # ...or behavior only
  - bundle: git+https://github.com/anderlpz/amplifier-bundle-adi@main#subdirectory=behaviors/adi.yaml
```

### Prerequisites (auto-offered on first run — no manual setup required)

ADI's convergence loop uses two external CLIs. **You do not have to install these
in advance.** The first time you run `/adi`, the orchestrator checks for them and,
if either is missing, tells you exactly what's missing and **offers to install it
for you — with your approval.** Nothing is installed silently.

- [Impeccable](https://impeccable.style) CLI — `npm install -g impeccable`
- [agent-browser](https://github.com/vercel-labs/agent-browser) CLI — `npm install -g agent-browser && agent-browser install`

If you'd rather set them up manually beforehand, the commands above are all you
need. (`npm` / Node.js must be present for either path.)

## Usage

ADI is **invoke-then-load**: nothing heavy is mounted into your session until you
explicitly call it. Run the convergence loop with the `/adi` slash command:

```
/adi <target>
```

`<target>` is a URL or a reference to a rendered UI target you want certified.

**Recommended first run — no live URL needed.** This repo ships a deliberately
flawed local pricing page so you can see the loop work immediately:

```
/adi ./examples/pricing.html
```

That target contains intentional slop for both tiers to catch (mixed units,
low-contrast text, magic numbers, non-semantic buttons, inverted hierarchy,
placeholder states). See [`examples/pricing.html`](examples/pricing.html) for
the annotated list, and ["What you get"](#what-you-get) below for an illustrative
run. Once you've seen it, point `/adi` at a real target:

```
/adi https://staging.example.com/pricing
```

`/adi` is the only front door. It delegates to the `adi-orchestrator` agent, which
mounts the full toolchain (browser-tester, the Design Intelligence Council,
`tool-impeccable`, `tool-dom-extract`) and runs the render → Tier 1 → Tier 2 → certify loop **in its own
isolated sub-session** — so your root session carries near-zero footprint until the
moment you invoke it. The orchestrator uses the `quality-gate` agent as the
independent authority that certifies both tiers passed on the same render.

> **Note:** the `/adi` skill is discoverable because this bundle wires `tool-skills`.
> If you compose ADI into another bundle, ensure a skills tool is present so the
> slash command is registered.

## What You Get

Here is an **illustrative** run of `/adi ./examples/pricing.html` — the recommended
first target, which ships with intentional flaws. This shows the shape of the
output; exact findings depend on the current Impeccable ruleset, the design
lenses, and the render. It is not a recorded transcript.

**Render matrix evaluated**

| Cell | Viewport | State | Interaction |
|------|----------|-------|-------------|
| 1 | mobile (375px) | populated | default |
| 2 | tablet (768px) | populated | default |
| 3 | desktop (1440px) | populated | default |

**Tier 1 — Impeccable (deterministic slop) → `FINDINGS`**

```
FINDINGS (7):
  [contrast]      .muted #b8b8b8 on #ffffff — 2.1:1, fails WCAG AA (needs ≥4.5:1)
  [contrast]      .btn.ghost #cfcfcf on #f4f4f4 — 1.3:1, fails WCAG AA
  [magic-number]  arbitrary values: padding:13px, margin:27px, width:341px
  [unit-mixing]   px, rem, em, % mixed with no consistent scale
  [color-token]   three near-identical blues: #2b6cff, #2d6dfe, #3a75ff
  [semantics]     clickable <div class="btn"> — not a <button>/<a>, no focus state
  [a11y]          <img src="logo.png"> missing alt text
→ Fix loop runs; Tier 2 does NOT start until Tier 1 is CLEAN.
```

**Tier 2 — Design Intelligence Council (7 lenses, on a Tier-1-CLEAN render)**

```
originality-critic   CONCERN  Generic SaaS-pricing template; nothing distinctive.
coherence-guardian   FAIL     Playful hero + corporate cards + alarmist footer tell three stories.
human-advocate       FAIL     Tiny tap targets, color-only signaling, no focus states exclude real users.
craft-inspector      FAIL     Placeholder states shipped: "Lorem ipsum", "TODO: price", dead "Coming soon".
context-tester       CONCERN  341px fixed cards overflow the 375px mobile viewport.
purpose-keeper       CONCERN  Visual emphasis points at "Basic" — the least valuable plan (hierarchy inversion).
emotion-reader       FAIL     Footer manufactures false urgency; CTAs give no real reason to click.
—
Synthesized verdict: FAIL. Dissent recorded: originality-critic rated CONCERN, not FAIL.
```

**Quality gate — independent certification**

```
VERDICT: NOT CERTIFIED

Render:   desktop/1440 · populated · default — ./examples/pricing.html
Tier 1:   CLEAN     — deterministic gate passed after fix loop
Tier 2:   FAIL      — council synthesized FAIL (coherence, inclusion, craft, affect)

Reasoning:
Tier 1 converged to CLEAN, but the Design Intelligence Council returned a
blocking FAIL: incoherent visual story, exclusionary interaction design,
shipped placeholder states, and manufactured urgency. Certification requires
BOTH tiers to pass on the same render. Address the four blocking lens findings,
re-render, and re-run — Tier 1 first, then Tier 2.
```

That `NOT CERTIFIED` block is the point: ADI refuses to certify hollow work, and
tells you exactly what to fix. Run it against a polished target and the same
loop returns `CERTIFIED` with the evidence recorded.

## The Convergence Loop

```
Render → Tier 1 (Impeccable) → Tier 2 (Design Council) → Verdict
   ↑                                                        |
   └────────── loop until both pass or escalate at 5 ───────┘
```

1. **Render** — Capture the artifact across the render matrix (viewport × state × interaction) as both screenshot and DOM Intelligence Package.
2. **Tier 1: Impeccable** — Fast, deterministic, free. 46 slop-detection patterns enforce a minimum bar of craftsmanship. Returns `CLEAN` or structured `FINDINGS`. Failures are fixed before Tier 2 runs.
3. **Tier 2: Design Council** — Semantic evaluation via 7 orthogonal lenses working from both the screenshot and the DOM Intelligence Package — knowing the mechanical foundation is already sound.
4. **Exit or loop** — Both tiers must pass on the same rendered artifact. If either fails, fixes are applied and the loop re-renders. Escalates to human review after 5 iterations.

## Components

| Deliverable | Description |
|-------------|-------------|
| **`/adi` skill** | User-invoked front door (`/adi <target>`); delegates to the orchestrator and mounts nothing until called |
| **adi-orchestrator agent** | Spawned by `/adi` in its own sub-session; owns the full toolchain and runs the convergence loop |
| **tool-impeccable** | CLI wrapper that invokes the Impeccable.style deterministic linter |
| **tool-dom-extract** | DOM Intelligence Package — structured DOM extraction for semantic evaluation |
| **quality-gate agent** | Independent authority that certifies both tiers passed on the same render |
| **convergence recipe** | YAML recipe orchestrating the Render → Tier 1 → Tier 2 → loop |
| **render matrix** | Viewport × state × interaction surface defining what gets evaluated |

## The Render Matrix

The render matrix defines the evaluation surface: **viewport × state × interaction**. Each cell is evaluated with dual input — a screenshot (what a human sees) and a DOM Intelligence Package (what the machine can reason about structurally). This dual-input approach lets Tier 2 evaluators ground their visual judgments in actual DOM structure, preventing hallucinated findings.

See [`context/render-matrix.md`](context/render-matrix.md) for the full specification.

## Vision

ADI is a composable design quality studio. Impeccable and the Design Council are the first two evaluators, but the architecture is designed for new evaluators to plug in as gaps are discovered. Each evaluator is an independent bundle that knows nothing about ADI — ADI is the fan-in composition layer that orchestrates their collaboration.

## Dependencies

| Bundle / Tool | Role |
|---------------|------|
| [amplifier-bundle-browser-tester](https://github.com/microsoft/amplifier-bundle-browser-tester) | Rendering + DOM extraction primitives |
| [amplifier-bundle-design-council](https://github.com/microsoft/amplifier-bundle-design-council) | Tier 2 semantic evaluator — Design Intelligence Council (7 orthogonal lenses) |
| Impeccable.style CLI | Tier 1 deterministic slop detection |

## Contributing

This project is not currently accepting external contributions.

## License

[MIT](LICENSE)
