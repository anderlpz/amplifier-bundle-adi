# Render Matrix

## What This Is

Real design is multi-device, multi-state, and agent-driven. A single screenshot of a single page state cannot tell you whether a component works. The render step in the ADI convergence loop evaluates a **render matrix** — a declared set of viewport × state × interaction cells — not a single screenshot.

browser-tester navigates the live page across every declared cell. On each cell's single page visit, three things happen with **no extra navigation**:

1. **Impeccable** inspects the live DOM/CSS (Tier 1 ground truth — mechanical slop detection).
2. **tool-dom-extract** extracts the DOM Intelligence Package (Tier 2 ground truth — what the design actually is).
3. **browser-tester** captures the screenshot (Tier 2 visual perception — what the design looks like).

One page visit, three outputs. This matters for cost and correctness: re-navigating per artifact risks state drift between what Impeccable inspected, what the DOM extractor captured, and what the screenshot shows. All three must come from the same render.

## Dimensions

A matrix cell is the intersection of all three dimensions below. Not every design needs all cells — the implementing agent or recipe declares which cells matter for the design under evaluation. A hero section might only need 3 viewport cells; a form component needs viewports × states × interactions.

| Dimension | Values |
|-----------|--------|
| **Viewport** | mobile (375px), tablet (768px), desktop (1440px) |
| **State** | empty, loading, populated, error, overflow |
| **Interaction** | default, hover, focus, active, disabled |

## Declaring a Matrix

A matrix is declared as a YAML block, either inline in recipe context or as a convention in the design brief. Each cell names its viewport, state, and interaction, plus optional overrides.

```yaml
render_matrix:
  base_url: "http://localhost:3000/components/user-card"
  cells:
    - viewport: mobile
      state: populated
      interaction: default
    - viewport: mobile
      state: populated
      interaction: hover
    - viewport: tablet
      state: empty
      interaction: default
    - viewport: desktop
      state: error
      interaction: default
      url: "http://localhost:3000/components/user-card?force_error=true"
      selectors:
        - ".user-card"
        - ".error-banner"
```

- `render_matrix.base_url` — the default URL used for every cell unless overridden.
- `cells` — the list of declared cells to evaluate. Each cell requires `viewport`, `state`, and `interaction`.
- `url` (optional, per cell) — overrides `base_url` for cells that need a distinct route or query param to reach a given state (e.g., forcing an error state).
- `selectors` (optional, per cell) — a list of CSS selectors scoping the DOM Intelligence Package extraction to specific elements, for targeted inspection instead of the full page.

## Viewport Shorthands

Named viewports resolve to fixed pixel dimensions:

| Name | Width | Height |
|------|-------|--------|
| `mobile` | 375px | 812px |
| `tablet` | 768px | 1024px |
| `desktop` | 1440px | 900px |

A cell may bypass the shorthand and give explicit dimensions instead:

```yaml
- viewport:
    width: 1920
    height: 1080
  state: populated
  interaction: default
```

## Convergence Criteria

**Both tiers must pass across all declared cells on the same render.** This is a binary AND across cells — there is no weighting or selective sampling in v1. A design that is perfect on desktop but broken at mobile does **not** pass. All cells carry equal weight; none can be skipped or discounted because other cells look good.

This applies to both tiers:

- **Tier 1 (Impeccable)** runs across the full matrix. It is fast enough that inspecting a dozen or more live page states costs almost nothing — a contrast issue that only shows up at mobile width gets caught here.
- **Tier 2 (Design Intelligence)** also runs across the full matrix. No selective sampling or optimization in v1; full coverage builds confidence in the system before any future cost-driven narrowing is considered.

## Dual-Input Evaluation

Each matrix cell produces **two artifacts** for Tier 2 evaluation, not just a screenshot. Both are extracted on the same live page visit as the Impeccable inspection — no extra navigation.

### Artifact 1 — Screenshot (visual perception)

What the design *looks like*. Evaluated by the vision model for composition, visual hierarchy, spacing feel, and aesthetic quality.

### Artifact 2 — DOM Intelligence Package (ground truth)

What the design *actually is*, extracted from the live page:

- **`accessibility_tree`** — roles, labels, hierarchy, tab order.
- **`computed_styles`** — colors, fonts, spacing, layout mode (flex/grid) for key elements.
- **`dom_structure`** — semantic HTML hierarchy, heading levels, component boundaries.
- **`layout_geometry`** — bounding boxes, overflow detection, stacking context, clipping.

Design Intelligence agents receive **both artifacts**. The vision model's perception ("this looks well-spaced") is cross-checked against the DOM ground truth rather than trusted alone. Heading hierarchy violations, accessibility gaps, and mismatches between visual appearance and computed values all become catchable this way — the appearance and the reality are reconciled, not assumed to agree.

## Summary

- One page visit per cell produces all three outputs: Impeccable inspection, DOM Intelligence Package, screenshot.
- A matrix cell = viewport × state × interaction.
- Not every design needs every cell — the implementing agent or recipe declares the relevant subset.
- All declared cells must pass, for both tiers, on the same render. No weighting, no partial credit.
- Tier 2 always receives both the screenshot and the DOM Intelligence Package so visual perception is checked against ground truth.
