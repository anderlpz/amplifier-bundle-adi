---
bundle:
  name: adi
  version: 0.1.0
  description: >
    Amplifier Design Intelligence (ADI) — composes deterministic slop detection
    (Impeccable) with semantic design evaluation (Design Intelligence) in an
    enforced convergence loop. The cheap deterministic gate runs first, the
    expensive semantic gate second, and an independent authority certifies both
    passed on the same rendered artifact.

includes:
  # Foundation base (tools, session config, hooks) — ADI's own pieces are agent-scoped
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  # ADI's own agents (adi-orchestrator, quality-gate) and the /adi skill front door.
  # Everything heavy — browser-tester, design-intelligence-enhanced, tool-impeccable,
  # tool-dom-extract, render-matrix context — is composed INSIDE adi-orchestrator and
  # only loads when that agent is spawned via /adi. See agents/adi-orchestrator.md.
  - bundle: adi:behaviors/adi
---

# Amplifier Design Intelligence (ADI)

> **"The cheap pass always runs before the expensive one — and both must pass on the same render."**

ADI is a fan-in composition bundle: the single entity that knows about all three pieces
it orchestrates. None of the composed pieces know ADI exists.

```
amplifier-bundle-adi
   └─ agents/adi-orchestrator.md (spawned via /adi, agent-scoped composition)
        ├─ includes → amplifier-bundle-browser-tester    (rendering + DOM extraction)
        ├─ includes → design-intelligence-enhanced       (Tier 2 evaluators)
        └─ wraps    → Impeccable.style CLI                (Tier 1 via modules/tool-impeccable)
```

This root bundle carries near-zero footprint: only the `/adi` skill and cheap
agent metadata (name + description) for `adi-orchestrator` and `quality-gate` are
registered here. None of the heavy sub-bundles, tools, or context load until you
run `/adi <target>`, which delegates to `adi-orchestrator` in its own isolated
child session.

## The Two Collaborators

- **Impeccable = gatekeeper (Tier 1).** Fast, deterministic, free. 46 slop-detection
  patterns enforce a minimum bar of craftsmanship. Returns `CLEAN` or structured `FINDINGS`.
- **Design Intelligence = evaluator (Tier 2).** Semantic evaluation of composition,
  hierarchy, and aesthetic judgment, working from both the screenshot and the DOM
  Intelligence Package — knowing the mechanical foundation is already sound.

The convergence recipe orchestrates their collaboration; the quality gate certifies
their agreement, as an independent authority that never authors the work it judges.
See `context/render-matrix.md` (loaded by `adi-orchestrator`) for the evaluation surface.

## Usage

```
/adi <target>
```

This is the only front door. It delegates to `adi-orchestrator`, which mounts the
full toolchain in its own session and runs the convergence loop, using
`quality-gate` as the independent certifying authority.

---

@foundation:context/shared/common-system-base.md
