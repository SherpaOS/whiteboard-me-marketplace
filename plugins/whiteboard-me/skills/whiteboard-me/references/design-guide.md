# Whiteboard-Me Design Guide

Read this before adapting `assets/template.html`. The template is a skeleton, not a form
to fill — adjust geometry to fit the approved content, and delete placeholder slots you
don't use (an empty `{{TOOL_10}}` node left in the output is a bug).

## The aesthetic

The look is "smart person explaining their life on a whiteboard": warm paper, navy ink,
one marker-orange accent, handwriting fonts, everything slightly imperfect.

- Fonts: **Caveat** for headings/names/arc titles (feels hand-lettered), **Kalam** for
  body (legible handwriting). Don't introduce other fonts.
- Palette (CSS vars in the template): ink `#1e2a5a`, orange `#d96f2e`, teal `#2e7d6b`,
  purple `#6b4fa0`, paper `#faf8f2`. Orange is reserved for values, role, and banner —
  if everything is orange, nothing is.
- Imperfection is deliberate: the irregular border-radius values, ±0.8° panel tilts, and
  dashed ring strokes ARE the sketch style. Don't "clean them up".
- Headshot: grayscale + slight contrast (already in CSS) reads as "pencil portrait".
  If a background-removal tool was used, keep the circular ink frame regardless.

## Geometry and placement

The three rings are centered at (800, 920) with radii 330 (bridge), 470 (people),
620 (tools). Place nodes with polar coordinates:

```
left = 800 + r·cos(θ)   top = 920 + r·sin(θ)     θ in degrees, 0° = east, 90° = south
```

Rules of thumb:

- Even angular spacing per ring, but **skip the sectors occupied by other elements**:
  side panels sit at 150°–210° and 330°–30°; the corner values own the top corners;
  the banner owns the bottom center. Nodes colliding with panels is the #1 layout bug.
- People-ring labels ≤ 3 short words ("State Auditors", "Budget Directors"). Tool-ring
  labels ≤ 4 words. Bridge phrases ≤ 7 words.
- With fewer items than the template's slots, respace evenly — don't leave gaps where
  deleted nodes were.
- The number of value slots is flexible: 2–4 per top corner stack, 2–4 in the bottom row.
  Value glosses are 8–14 words. Longer than that, compress the language.

## Icon choice

Emoji glyphs are fine and keep the file self-contained. Pick semantically obvious ones
(👥 for audiences, 🏛 for government/institutions, ⚙️/🤖/📊 for tools). If emoji feel
wrong for the person's brand, swap the `.glyph` spans for small inline SVG sketches —
but only if you have time budget; emoji ship first.

Portrait: prefer the bundled `scripts/sketch_portrait.py` output (base64-embedded JPEG/PNG)
over CSS filters — blend modes don't survive headless rendering, and the script's hatched
ink style matches the ring line-work. Tune `--blur` (10-18) if lines are too heavy/faint.

Collaborator rule (non-negotiable): generic glyphs only. Never render, fetch, or invent
a real person's likeness for ring nodes unless the user explicitly supplied that photo.

## Verifying the render

Always look at what you made before the user does:

1. Screenshot the HTML headlessly if possible:
   `npx -y playwright screenshot --viewport-size=1600,2000 file.html out.png`
   (install chromium via `npx playwright install chromium --with-deps` if needed;
   if the sandbox can't, fall back to any available render/preview tool).
2. Check for: overlapping text, nodes touching panels, clipped banner (it's
   `white-space: nowrap` — long taglines overflow), orphaned placeholder `{{...}}` text,
   emoji that failed to render.
3. Fix, re-screenshot, then deliver.

## Recomposition for other formats

- **Square (1:1, 1600×1600)**: drop the bottom values row, move banner up, tighten ring
  radii ~15%.
- **Story (9:16, 1080×1920)**: stack instead of radial — center block top, panels mid,
  values bottom. Keep the arc title as a straight marker-underlined heading.
- Never scale-and-crop the 4:5 master; recompose.
- The `⛰ made with Sherpa OS` watermark stays bottom-right in every variant (signature-sized,
  pencil tone). Remove only on explicit user request.
