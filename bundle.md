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
  # Rendering + DOM extraction primitives (screenshots, viewports, accessibility tree)
  - bundle: git+https://github.com/microsoft/amplifier-bundle-browser-tester@main
  # Tier 2 semantic evaluators (design-check, art-director, research-analyst)
  - bundle: git+https://github.com/anderlpz/amplifier-bundle-design-intelligence-enhanced@main
  # ADI's own tools, quality-gate agent, and render-matrix context
  - bundle: adi:behaviors/adi
---

# Amplifier Design Intelligence (ADI)

> **"The cheap pass always runs before the expensive one — and both must pass on the same render."**

ADI is a fan-in composition bundle: the single entity that knows about all three pieces
it orchestrates. None of the composed pieces know ADI exists.

```
amplifier-bundle-adi
   ├─ includes → amplifier-bundle-browser-tester    (rendering + DOM extraction)
   ├─ includes → design-intelligence-enhanced       (Tier 2 evaluators)
   └─ wraps    → Impeccable.style CLI                (Tier 1 via modules/tool-impeccable)
```

## The Two Collaborators

- **Impeccable = gatekeeper (Tier 1).** Fast, deterministic, free. 46 slop-detection
  patterns enforce a minimum bar of craftsmanship. Returns `CLEAN` or structured `FINDINGS`.
- **Design Intelligence = evaluator (Tier 2).** Semantic evaluation of composition,
  hierarchy, and aesthetic judgment, working from both the screenshot and the DOM
  Intelligence Package — knowing the mechanical foundation is already sound.

The convergence recipe orchestrates their collaboration; the quality gate certifies
their agreement. See `context/render-matrix.md` for the evaluation surface.

---

@foundation:context/shared/common-system-base.md
