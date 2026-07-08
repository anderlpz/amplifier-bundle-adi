# Amplifier Design Intelligence (ADI)

A two-tier convergence loop for design quality — Impeccable keeps the floor clean (deterministic slop detection on live DOM), the Design Intelligence Council focuses on the ceiling (7-lens semantic evaluation). Both must pass on the same render for the loop to exit.

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
