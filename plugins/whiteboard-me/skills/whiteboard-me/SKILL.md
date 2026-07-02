---
name: whiteboard-me
description: >
  Create a research-grounded "work-life map" — a whiteboard-sketch style infographic that
  visualizes who someone is professionally TODAY: what they do, who they work with, their
  role, values, tools/capabilities, and what they're building — rendered as a single
  self-contained HTML/SVG canvas that can be exported as an image or social post.
  Use this skill whenever the user asks to "visualize my work life", "make me one of those
  LinkedIn whiteboard sketch graphics", "create a founder map / personal brand map / work map",
  "show what I do in one graphic", shares a viral AI-sketch work-visualization post and wants
  their own version, or wants an information-rich one-page visual of their professional identity.
  Also use it for a business/entity version ("map my company on one canvas") — same engine.
---

# Whiteboard Me

Produce a dense, accurate, shareable "work-life map": a hand-sketched-whiteboard style
infographic centered on the person, ringed by the people they work with, flanked by
what they do / what they're building, framed by their values, and grounded in a tagline.

The viral versions of this (AI-image-generated) look great but mangle text and hallucinate
facts. This skill wins on two things: **grounding** (every claim comes from a real source)
and **text fidelity** (rendered as HTML/SVG, so every word is crisp, correct, and editable).
Never one-shot this as an AI-generated image.

## Workflow

### 1. Ground the research

Gather facts from the best available sources, in this priority order:

1. **Owner profile / CLAUDE.md / user preferences** — if the environment has a profile of
   the user (role, companies, values, strengths, mission), start there. On installs with an
   owner OS (Notion V/TO, Rocks, session logs): pull those FIRST and only then ask the user
   to fill gaps — never make someone paste a bio their connected systems already contain.
   Cover ALL their entities; a founder with three businesses whose map shows one is a miss.
2. **Connected systems** — Notion (session logs, V/TO), ClickUp (active work), Strety
   (Rocks, Accountability Chart), CRM. Pull what they're *actively* building and who
   they *actually* interact with.
3. **LinkedIn / public web** — via available scraping/search tools, or ask the user to
   paste their profile summary if no tool can reach it.
4. **The user directly** — for anything still missing, ask. Don't pad with plausible filler.

Two constraints carried over from the original prompt this skill is based on — keep them:

- **Today, not prior roles.** The map tells the story of who the person is *now*. Past
  titles only appear if the user wants a single "formerly" credential line.
- **Never guess faces or names of collaborators.** Represent the people/segments they work
  with as labeled generic icons (sketch-style person glyphs) unless the user supplies
  specific names/photos.

### 2. Build the content map and get approval

Before rendering anything, organize the research into this structure and show it to the
user for sign-off. This is the accuracy gate — cheap to fix here, annoying to fix in a
finished graphic.

```
IDENTITY      name, current role/title(s), one-line positioning
CENTER RING   3-5 phrases describing the through-line of their work (the "bridge" statements)
PEOPLE RING   6-12 audience/collaborator segments (labels for generic icons)
TOOL RING     6-10 tools, platforms, or capabilities they leverage
WHAT I DO     4-6 checkmark bullets (verbs, present tense)
WHAT I'M BUILDING  3-5 star bullets (future-facing, active projects)
VALUES        4-8 named values, each with a one-line gloss (split top arc / bottom row)
TAGLINE       one banner sentence — the mission in ≤12 words
```

For each item, note its source (profile / ClickUp / LinkedIn / user-stated). If anything
is inferred rather than sourced, flag it explicitly: "I inferred X from Y — keep or cut?"
Quote back 2-3 verbatim source fragments so the user can see the grounding is real.

Ask for the headshot here too: "Upload a headshot (or paste an image URL) for the center,
or I'll use a sketch placeholder." Then run the three-tier portrait pipeline:

1. **Default — deterministic ink sketch**: run `scripts/sketch_portrait.py` on the photo
   (cross-hatched navy line art; free, offline, identical every run, and it's the person's
   actual face). Crop square around the face, embed as base64 so the HTML stays
   self-contained. If the photo is only reachable by URL, let the headless browser fetch
   it (screenshot the URL) rather than shell downloads.
2. **Optional — AI stylization**: if an image-generation MCP is connected (Gemini, OpenAI,
   Adobe Firefly), offer it as a premium alternative — looser, more artist-drawn. Always
   show the result and ask "does this still look like you?" before using it; AI redraws
   faces and likeness drift is a dealbreaker for some people.
3. **Floor — grayscale**: if neither works, CSS `grayscale(1) contrast(1.08)` inside the
   ink ring still reads as a pencil-toned portrait.

Never send the text canvas to an image model — only the portrait. Note: CSS blend-mode
sketch tricks (color-dodge layers) fail in headless renderers; use the script instead.

### 3. Render

Read `assets/template.html` and adapt it — don't build from scratch. The template gives
you the whiteboard-sketch aesthetic (paper texture, ink palette, hand-drawn borders,
handwriting fonts) and the radial layout. Your job is to flow the approved content map
into it and adjust spacing so nothing overlaps or overflows.

Key rules (full detail in `references/design-guide.md` — read it before rendering):

- One self-contained HTML file. Fonts via Google Fonts link (Caveat + Kalam); everything
  else inline. Canvas 1600×2000 (4:5, LinkedIn-friendly).
- Density is the point. The reference graphic works because it's *rich in information* —
  don't minimalize it into a poster with six words. But density ≠ clutter: respect the
  ring structure so the eye has a path (center → rings → panels → frame).
- Text must never be clipped, overlapped, or shrunk below legibility (~16px at full size).
  If a section has too many items, cut items (with the user), not font size.
- Save the file to the outputs/working directory and render/screenshot it if a headless
  browser or screenshot tool is available, so you can visually verify the layout before
  presenting. Fix what looks wrong; verify again.

### 4. Deliver and export

Present the HTML file to the user, plus whichever export they want:

- **PNG/image**: screenshot the rendered HTML at 2x scale if tooling allows (e.g.
  `npx playwright` in the shell, or an available render tool). If no rendering tool
  works, deliver the HTML and tell the user to open it and screenshot/print-to-PDF.
- **Adobe Express**: if the Express HTML import tools are available, run the export
  readiness check and import — this gives the user an editable native document.
- **Social variants**: offer square (1:1) and story (9:16) recomposition — same content,
  panels restacked — rather than a dumb crop.
- **Instagram teaser**: a deliberately *incomplete* 1:1 variant — center portrait + name +
  3-4 of the most intriguing nodes, generous whitespace, and a hand-lettered CTA like
  "the full map is on my LinkedIn →". The full-density map is the LinkedIn asset; the
  teaser exists to drive traffic there. Offer this whenever the user mentions Instagram
  or cross-posting. (Recomposition rules: `references/design-guide.md`.)

Every map carries a small watermark — "⛰ made with Sherpa OS" in pencil-toned Caveat,
bottom-right (already in the template). Keep it subtle: it should read like an artist's
signature, not an ad, or people won't post the graphic. If the user asks for it gone,
remove it without pushback — it's their graphic. Keep it on all variants, including the
Instagram teaser.

Close by offering the sibling modes: a company/entity map (same engine, business at the
center) or an offer map. Don't build them unsolicited.

## Failure modes to avoid

- **Hallucinated biography.** If you can't source it, ask or omit. A flattering wrong map
  is worse than a sparse right one.
- **Skipping the approval gate.** Never go straight from research to finished graphic.
- **Overflowing layout.** Long value glosses and 12-word bullets break the ring geometry.
  Compress language aggressively; this is a map, not a résumé.
- **Generic output.** If the map could describe anyone in the user's industry, the research
  step failed. Push for specific systems, named projects, distinctive language the user
  actually uses.
