# v0.2 locked spec — proven across a live 8-iteration build (2026-07-02)

Treat this as the DEFAULT rendering spec. It supersedes conflicting guidance in
design-guide.md. Every rule below was earned by a real failure in the first
live build; don't relearn them.

## Canvas: landscape 2000×1300 (not portrait)

Landscape matches the viral reference format and LinkedIn's feed. Rings
centered (1000,700), radii 280 / 390 / 500.

## Rings: solid drawn strokes — NEVER dashed

Dashes read as "software diagram." A hand draws one continuous wobbly line and
retraces it. Implementation:
- 3 stacked passes per ring: main stroke (opacity ~.6) + two echoes at ±1°
  rotation and ±1-2px radius, opacity .3 / .18, thinner.
- Each pass wrapped in an SVG filter: `feTurbulence` (fractalNoise,
  baseFrequency .008–.014, 3 octaves, distinct seeds) → `feDisplacementMap`
  scale 10–14.
- A finer filter (baseFrequency .045, scale ~2.6) applied via CSS to `.panel`,
  `.banner`, the portrait ring, and every icon SVG so no stroke on the canvas
  is geometrically perfect.

## Zoning (the collision-free arrangement)

- **Ring titles own the top.** Main title arc above everything; tools-ring
  title on an arc BETWEEN the people and tools circles (r≈445 apex); people
  title between bridge and people circles (r≈335 apex). Nothing else may
  occupy 10pm–2am on any ring.
- **Nodes live IN the bands, on the 2→10 o'clock arc only.** People at r≈335
  (band 280–390), tools at r≈447 (band 390–500). Node width ≤140px — wider
  nodes touch both circles near 3 and 9 o'clock (radial span = half-width
  there). Even angular spacing; per-node rotation ±2°.
- **Bridge phrases CURVE on nested arcs above the portrait** — SVG textPath on
  concentric arcs inside the inner ring (e.g. r≈255 apex then r≈212 apex), so
  the top of the map reads as four nested arcs of hand-lettering (main title →
  tools title → people title → bridge phrases). One phrase below the roles
  line stays straight to anchor the text block. Never place bridges at
  ring-edge 2/10 o'clock — they collide with the corner nodes.
- **Values: 3 per side on the far left/right edges. Panels: BELOW the rings**
  in the bottom corners (never mid-height — they trap ring nodes). Banner
  bottom-center; watermark corner.

## Icons: hand-drawn stroke SVGs, never emoji

Emoji read as pasted clip-art ("ChatGPT-ish"). Use inline SVG line icons:
viewBox 48, stroke-width 2.6, round caps/joins, currentColor, ~46px. Draw
sketch-style LOGO marks for recognizable software (Claude starburst, Notion
N-page, ClickUp chevron, GitHub octocat outline, n8n node-chain, GHL steps…)
and monogram marks for the owner's own brands — offer to trace real logo files
if the user has them. Handwriting fonts lack → and ⛰ glyphs — in raster
compositions draw arrows/mountains as strokes or they render as tofu boxes.
(SVG/HTML text gets per-glyph browser fallback, so → is safe there.)

## Portrait tiers (the make-or-break element — iterate here hardest)

1. **BEST — AI sketch redraw with the reference photo attached** (Gemini /
   nano-banana, prompt in `assets/gemini-portrait-prompt.txt`). Likeness gate:
   the user must confirm it still looks like them. If no image-gen tool is
   connected, hand the user the prompt to run in their Gemini app and embed
   their result.
2. **Adobe `image_vectorize`** (Firefly connector) → gradient-map the result:
   tight face crop + S-curve contrast (×1.4 around mid) BEFORE mapping, then
   B&W graphite or brand-duotone stops. Without the S-curve the face washes
   out; without the crop it drowns in shirt.
3. **`scripts/sketch_portrait.py`** — deterministic fallback.

Remove the CSS grayscale filter from the portrait `<img>` when embedding
pre-toned art. Compress embeds: 560px, quantize ≤64 colors (≤30–180KB).

## Distribution add-ons (offer after the map is approved)

- **IG teaser** (1080×1080 PNG, composed in PIL): circle-cropped portrait with
  wobble-drawn ring, name + role line, 3 intriguing hooks with drawn arrows,
  bordered CTA "the full map is on my LinkedIn" + drawn arrow, watermark.
  Fonts: fetch Caveat/Kalam TTFs via fonts.googleapis.com/css2 → gstatic URLs.
- **GHL Social Planner staging** (where a GoHighLevel connector is present):
  `social-media-posting_get-account` → if accounts exist, `create-post` as a
  DRAFT per chosen account with the caption + hosted media URL; never publish
  directly without explicit approval. If `accounts` comes back EMPTY the GHL
  location has no social profiles attached — direct the owner to GHL →
  Marketing → Social Planner → connect accounts, then stage.
