#!/usr/bin/env python3
"""
sketch_portrait.py — deterministic pencil/ink-sketch portrait for whiteboard-me.

Converts a headshot into cross-hatched ink line art matching the whiteboard
aesthetic (navy ink on paper). No AI, no network: identical output every run,
and it's the person's actual face — no likeness drift.

Usage:
    python3 sketch_portrait.py input.jpg output.png [--ink 1e2a5a] [--paper faf8f2]

Technique: dodge-blend line extraction (gray / (255 - blurred inverse)) for
line work, plus diagonal + cross hatching in genuinely dark regions so suits
and backdrops read as hand-shaded rather than photographic. Requires Pillow
and numpy (both standard in the sandbox).
"""
import sys
import argparse
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def sketch(src, dst, ink="1e2a5a", paper="faf8f2", blur=14):
    im = Image.open(src).convert('L')
    g = np.asarray(im).astype('float32')
    h, w = g.shape

    # 1) dodge line-art: bright areas -> paper, edges -> ink lines
    inv = ImageOps.invert(im).filter(ImageFilter.GaussianBlur(blur))
    b = np.asarray(inv).astype('float32')
    lines = np.clip(g * 255.0 / (256.0 - b), 0, 255)

    # 2) darkness map (smoothed) — where a human would shade
    dk_img = Image.fromarray((255 - g).astype('uint8')).filter(ImageFilter.GaussianBlur(3))
    dk = np.asarray(dk_img).astype('float32') / 255.0

    # 3) hand-shading: diagonal hatch on dark areas, cross-hatch on darkest
    yy, xx = np.mgrid[0:h, 0:w]
    hatch1 = (((xx + yy) % 8) < 2).astype('float32')
    hatch2 = (((xx - yy) % 10) < 2).astype('float32')
    shade = np.clip(dk - 0.35, 0, 1) / 0.65          # ignore mid-tones
    strength = shade * hatch1 * 150 + (shade > 0.75) * hatch2 * 90

    out = np.clip(lines - strength, 0, 255).astype('uint8')
    res = ImageOps.colorize(Image.fromarray(out), black=hex_rgb(ink), white=hex_rgb(paper))
    res = ImageEnhance.Contrast(res).enhance(1.05)
    res.save(dst)
    print(f"sketch written: {dst} ({res.size[0]}x{res.size[1]})")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--ink", default="1e2a5a")
    p.add_argument("--paper", default="faf8f2")
    p.add_argument("--blur", type=int, default=14, help="dodge blur radius; higher = softer lines")
    a = p.parse_args()
    sketch(a.input, a.output, a.ink, a.paper, a.blur)
