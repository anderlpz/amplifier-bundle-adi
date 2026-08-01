# Amplifier Design Intelligence (ADI)

A two-tier convergence loop for design quality — Impeccable keeps the floor clean (deterministic slop detection on live DOM), the Design Intelligence Council focuses on the ceiling (7-lens semantic evaluation). Both must pass on the same render for the loop to exit.

## Installation

One command to add, one to activate — then start a session and use `/adi`. Same
flow as `/design-council` and the other `/`-command bundles:

```bash
# 1. Add the bundle (fetches from GitHub, registers it)
amplifier bundle add git+https://github.com/anderlpz/amplifier-bundle-adi@main

# 2. Activate it
amplifier bundle use adi

# 3. Start a fresh session — /adi is now available
amplifier run
```

Then in the session:

```
/adi https://staging.example.com/pricing
```

Prefer `/adi` alongside your everyday workflow instead of switching bundles?
Include it in your own bundle's `bundle.md` — it composes cleanly next to
design-council and other `/`-command bundles:

```yaml
includes:
  - bundle: git+https://github.com/anderlpz/amplifier-bundle-adi@main
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

```
/adi https://staging.example.com/pricing
```

`/adi` is the only front door. It delegates to the `adi-orchestrator` agent, which
mounts the full toolchain (browser-tester, design-intelligence, `tool-impeccable`,
`tool-dom-extract`) and runs the render → Tier 1 → Tier 2 → certify loop **in its own
isolated sub-session** — so your root session carries near-zero footprint until the
moment you invoke it. The orchestrator uses the `quality-gate` agent as the
independent authority that certifies both tiers passed on the same render.

> **Note:** the `/adi` skill is discoverable because this bundle wires `tool-skills`.
> If you compose ADI into another bundle, ensure a skills tool is present so the
> slash command is registered.

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
| [amplifier-bundle-design-intelligence-enhanced](https://github.com/anderlpz/amplifier-bundle-design-intelligence-enhanced) | Tier 2 semantic evaluators |
| [amplifier-bundle-design-council](https://github.com/anderlpz/amplifier-bundle-design-council) | 7-lens design evaluation council |
| Impeccable.style CLI | Tier 1 deterministic slop detection |

## Contributing

This project is not currently accepting external contributions.

## License

[MIT](LICENSE)
