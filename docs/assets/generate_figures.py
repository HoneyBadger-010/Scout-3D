# Generates the README figures for Scout (Team Honeybadger).
# Output: banner.png plus SVG diagrams in this folder.
# Usage: python docs/assets/generate_figures.py
# Requires Pillow and numpy. Figures describe the system design (SCOUT.md);
# all numbers are design targets or worked calculations, not measured results.

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

BG = '#0B1B2B'
PANEL = '#10263A'
PANEL_2 = '#15304A'
BORDER = '#21405C'
TEAL = '#3FB3CF'
TEAL_D = '#1A7A96'
NAVY = '#0E3A5F'
CORAL = '#FF7A66'
AMBER = '#F5B342'
RED = '#FF6470'
GREY = '#6B7785'
TEXT = '#E6EEF5'
MUTED = '#9AAEC0'
FAINT = '#5F7488'
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


def Esc(text):
	return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def Svg(width, height, body):
	return (
		f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
		f'font-family="{FONT}">\n'
		'<defs>\n'
		f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
		f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>\n'
		f'<marker id="arrowTeal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
		f'<path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>\n'
		f'<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
		f'<rect width="9" height="9" fill="{CORAL}" fill-opacity="0.18"/><line x1="0" y1="0" x2="0" y2="9" stroke="{CORAL}" stroke-width="3" stroke-opacity="0.55"/></pattern>\n'
		f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>'
		'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
		'</defs>\n'
		f'<rect width="{width}" height="{height}" rx="18" fill="{BG}"/>\n'
		f'{body}\n</svg>\n'
	)


def Text(x, y, text, size=14, fill=TEXT, weight=400, anchor='start', mono=False, spacing=0, opacity=1):
	family = f' font-family="{MONO}"' if mono else ''
	extra = f' letter-spacing="{spacing}"' if spacing else ''
	op = f' fill-opacity="{opacity}"' if opacity != 1 else ''
	return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{family}{extra}{op}>{Esc(text)}</text>'


def Header(label, title, x=40):
	return Text(x, 46, label, 12, TEAL, 500, mono=True, spacing=3) + '\n' + Text(x, 78, title, 23, TEXT, 600)


def Write(name, content):
	with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
		f.write(content)
	print('wrote', name)


# ------------------------------------------------------------------ pipeline

def Box(x, y, w, h, number, lines, tech, accent=False):
	stroke = TEAL if accent else BORDER
	fill = PANEL_2 if accent else PANEL
	parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{2 if accent else 1.5}"'
		+ (' filter="url(#glow)"' if accent else '') + '/>']
	parts.append(Text(x + 14, y + 24, f'{number:02d}', 11, TEAL, 600, mono=True, spacing=1))
	for i, line in enumerate(lines):
		parts.append(Text(x + 14, y + 46 + i * 19, line, 16 if accent else 15, TEXT, 600))
	parts.append(Text(x + 14, y + h - 13, tech, 10.5, MUTED, 400, mono=True))
	return '\n'.join(parts)


def Pipeline():
	w, h = 1200, 560
	b = [Header('SCOUT · 14-STEP PIPELINE', 'Two tracks with opposite weaknesses, fused at step 7')]
	# phase brackets
	b.append(f'<path d="M40,112 L40,104 L760,104 L760,112" fill="none" stroke="{FAINT}" stroke-width="1.5"/>')
	b.append(Text(48, 98, 'IN FLIGHT · steps 1–6 stream while the drone is airborne', 11, MUTED, 500, mono=True, spacing=1))
	b.append(f'<path d="M790,112 L790,104 L1160,104 L1160,112" fill="none" stroke="{FAINT}" stroke-width="1.5"/>')
	b.append(Text(798, 98, 'AFTER LANDING · steps 7–14', 11, MUTED, 500, mono=True, spacing=1))

	bw, bh = 160, 100
	a_y, m_y, b_y = 146, 244, 342
	mid = bh // 2
	b.append(Text(420, a_y - 12, 'TRACK A · ALGORITHMIC GEOMETRY — accurate, full of holes', 10.5, TEAL, 500, mono=True, spacing=1))
	b.append(Text(420, b_y + bh + 22, 'TRACK B · LEARNED PRIORS — complete, no scale', 10.5, CORAL, 500, mono=True, spacing=1))

	b.append(Box(40, m_y, bw, bh, 1, ['Ingest'], 'FFmpeg · SRT · KLV'))
	b.append(Box(222, m_y, bw, bh, 2, ['Keyframe', 'selection'], 'sharp · glare · ΔGPS'))
	b.append(Box(420, a_y, bw, bh, 3, ['Tie points'], 'SuperPoint · LightGlue'))
	b.append(Box(600, a_y, bw, bh, 4, ['Camera poses +', 'metric scale'], 'COLMAP · Ceres · GPS'))
	b.append(Box(420, b_y, bw, bh, 5, ['Semantic', 'segmentation'], 'SegFormer · UAVid'))
	b.append(Box(600, b_y, bw, bh, 6, ['Monocular', 'depth'], 'Depth Anything V2'))
	b.append(Box(800, m_y - 12, 160, bh + 24, 7, ['Scale', 'alignment'], 'robust a·d + b fit', accent=True))

	arrow = f'fill="none" stroke="{MUTED}" stroke-width="1.8" marker-end="url(#arrow)"'
	b.append(f'<path d="M200,{m_y + mid} L218,{m_y + mid}" {arrow}/>')
	b.append(f'<path d="M382,{m_y + mid - 16} C400,{m_y + mid - 16} 396,{a_y + mid} 416,{a_y + mid}" {arrow}/>')
	b.append(f'<path d="M382,{m_y + mid + 16} C400,{m_y + mid + 16} 396,{b_y + mid} 416,{b_y + mid}" {arrow}/>')
	b.append(f'<path d="M580,{a_y + mid} L596,{a_y + mid}" {arrow}/>')
	b.append(f'<path d="M580,{b_y + mid} L596,{b_y + mid}" {arrow}/>')
	b.append(f'<path d="M760,{a_y + mid} C784,{a_y + mid} 776,{m_y + mid - 16} 796,{m_y + mid - 16}" fill="none" stroke="{TEAL}" stroke-width="2" marker-end="url(#arrowTeal)"/>')
	b.append(f'<path d="M760,{b_y + mid} C784,{b_y + mid} 776,{m_y + mid + 16} 796,{m_y + mid + 16}" fill="none" stroke="{CORAL}" stroke-width="2" marker-end="url(#arrow)"/>')
	# masks feed pose estimation
	b.append(f'<path d="M470,{b_y - 2} L470,{a_y + bh + 4}" fill="none" stroke="{FAINT}" stroke-width="1.5" stroke-dasharray="5 5" marker-end="url(#arrow)"/>')
	b.append(Text(478, m_y + 42, 'masks cars, people,', 10, FAINT, 400, mono=True))
	b.append(Text(478, m_y + 56, 'sky before poses', 10, FAINT, 400, mono=True))

	rows = ['Fusion + confidence', 'Mesh extraction', 'Building completion', 'Texture + seams', 'Georeference + export', 'Analysis overlays', 'Serve + spatial query']
	lx, ly, lw, lh = 995, 140, 165, 42
	for i, row in enumerate(rows):
		y = ly + i * (lh + 6)
		b.append(f'<rect x="{lx}" y="{y}" width="{lw}" height="{lh}" rx="9" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
		b.append(Text(lx + 12, y + 25, f'{i + 8:02d}', 10.5, TEAL, 600, mono=True))
		b.append(Text(lx + 38, y + 25, row, 12.5, TEXT, 500))
	b.append(f'<path d="M960,{m_y + mid} L978,{m_y + mid}" {arrow}/>')
	b.append(f'<path d="M985,{ly + 4} L982,{ly + 4} L982,{ly + 7 * 46 - 10} L985,{ly + 7 * 46 - 10}" fill="none" stroke="{FAINT}" stroke-width="1.5"/>')

	b.append(Text(40, 528, 'AI depth is complete but has no scale. Sparse geometry has scale but is full of holes. Step 7 makes each fix the other.', 13, MUTED, 400))
	Write('pipeline.svg', Svg(w, h, '\n'.join(b)))


# ------------------------------------------------------------------ baseline

def Camera(x, y, color):
	return (f'<path d="M{x - 12},{y - 8} L{x + 12},{y - 8} L{x + 7},{y + 6} L{x - 7},{y + 6} z" fill="{PANEL_2}" stroke="{color}" stroke-width="1.8"/>'
		f'<circle cx="{x}" cy="{y - 1}" r="3" fill="{color}"/>')


def Baseline():
	w, h = 1200, 520
	b = [Header('WHY SINGLE-PASS IS HARD', 'Depth accuracy is set by the baseline, not by the frame count')]
	ground = 372

	def Panel(x0, title, sub, c1, c2, ex, ey, rx, ry, color, value):
		p = [f'<rect x="{x0}" y="112" width="290" height="352" rx="14" fill="{PANEL}" stroke="{BORDER}"/>']
		p.append(Text(x0 + 20, 142, title, 15, TEXT, 600))
		p.append(Text(x0 + 20, 162, sub, 11, MUTED, 400, mono=True))
		p.append(f'<line x1="{x0 + 20}" y1="{ground}" x2="{x0 + 270}" y2="{ground}" stroke="{FAINT}" stroke-dasharray="4 5"/>')
		for cx in (c1, c2):
			p.append(f'<line x1="{cx}" y1="206" x2="{ex}" y2="{ey - ry}" stroke="{color}" stroke-opacity="0.5" stroke-width="1.2"/>')
			p.append(f'<line x1="{cx}" y1="206" x2="{ex}" y2="{ey + ry}" stroke="{color}" stroke-opacity="0.5" stroke-width="1.2"/>')
		p.append(f'<ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="{color}" fill-opacity="0.22" stroke="{color}" stroke-width="1.8"/>')
		p.append(Camera(c1, 200, color))
		p.append(Camera(c2, 200, color) if c2 != c1 else '')
		p.append(Text(x0 + 145, 432, value, 30, color, 700, anchor='middle'))
		p.append(Text(x0 + 145, 452, 'depth error at 100 m', 11, MUTED, 400, anchor='middle', mono=True))
		return '\n'.join(p)

	b.append(Panel(40, 'Adjacent video frames', 'B = 0.5 m · 1/30 s apart', 182, 190, 186, 318, 7, 70, CORAL, '±3.7 m'))
	b.append(Panel(350, 'Distance-gated keyframes', 'B = 20 m · 40 frames apart', 400, 590, 495, 330, 9, 5, TEAL, '±9 cm'))

	# log-scale chart
	x0, px_per_decade = 700, 108
	def X(v):
		return x0 + (math.log10(v) + 2) * px_per_decade
	b.append(f'<rect x="670" y="112" width="490" height="352" rx="14" fill="{PANEL}" stroke="{BORDER}"/>')
	b.append(Text(690, 142, 'Depth error σZ at 100 m altitude', 15, TEXT, 600))
	b.append(Text(690, 162, 'log scale · 4K camera, f ≈ 2700 px, σd = 0.5 px', 11, MUTED, 400, mono=True))
	rows = [
		('Onboard stereo pair', 'B = 0.1 m', 18.5, GREY, '±18.5 m'),
		('Adjacent frames', 'B = 0.5 m', 3.7, CORAL, '±3.7 m'),
		('Keyframes (ours)', 'B = 20 m', 0.093, TEAL, '±9 cm'),
	]
	for i, (name, base, value, color, label) in enumerate(rows):
		y = 192 + i * 64
		b.append(Text(690, y, name, 13, TEXT, 600))
		b.append(Text(840, y, base, 11, MUTED, 400, mono=True))
		b.append(f'<rect x="{x0}" y="{y + 10}" width="{X(value) - x0:.1f}" height="16" rx="4" fill="{color}" fill-opacity="0.85"/>')
		b.append(Text(X(value) + 8, y + 23, label, 12, color, 700, mono=True))
	y = 192 + 3 * 64
	b.append(Text(690, y, 'Cross-track', 13, TEXT, 600))
	b.append(Text(840, y, 'B ≈ 0', 11, MUTED, 400, mono=True))
	b.append(f'<line x1="{x0}" y1="{y + 18}" x2="1130" y2="{y + 18}" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrow)"/>')
	b.append(Text(1000, y + 4, 'unbounded', 12, RED, 700, mono=True))
	b.append(f'<line x1="{x0}" y1="434" x2="{X(100)}" y2="434" stroke="{FAINT}"/>')
	for v, lab in [(0.01, '1 cm'), (0.1, '10 cm'), (1, '1 m'), (10, '10 m'), (100, '100 m')]:
		b.append(f'<line x1="{X(v):.1f}" y1="430" x2="{X(v):.1f}" y2="438" stroke="{FAINT}"/>')
		b.append(Text(X(v), 452, lab, 10.5, MUTED, 400, anchor='middle', mono=True))

	b.append(Text(40, 494, 'σZ = Z² / (f · B) · σd   —   error grows with the square of distance and falls with the baseline. Video gives redundancy, not viewpoint diversity.', 12.5, MUTED, 400, mono=True))
	Write('baseline.svg', Svg(w, h, '\n'.join(b)))


# ------------------------------------------------------------------ keyframes

def Keyframes():
	w, h = 1200, 360
	rng = random.Random(158)
	b = [Header('STEP 2 · KEYFRAME SELECTION', 'We throw away 97% of the video on purpose')]
	b.append(Text(1160, 60, '18,000 → 450', 30, TEAL, 700, anchor='end'))
	b.append(Text(1160, 80, 'frames in · keyframes out (10-min flight)', 11, MUTED, 400, anchor='end', mono=True))

	# full flight timeline with the zoomed minute highlighted
	x0, x1 = 40, 1160
	b.append(Text(x0, 118, 'FULL FLIGHT · 10:00 · 18,000 FRAMES', 10.5, MUTED, 500, mono=True, spacing=1))
	b.append(f'<rect x="{x0}" y="126" width="{x1 - x0}" height="14" rx="4" fill="{PANEL_2}"/>')
	for t1, t2 in [(0.22, 0.235), (0.61, 0.628)]:
		b.append(f'<rect x="{x0 + (x1 - x0) * t1:.1f}" y="126" width="{(x1 - x0) * (t2 - t1):.1f}" height="14" fill="{GREY}" fill-opacity="0.6"/>')
	zx1, zx2 = x0 + (x1 - x0) * 0.40, x0 + (x1 - x0) * 0.50
	b.append(f'<rect x="{zx1:.1f}" y="123" width="{zx2 - zx1:.1f}" height="20" rx="4" fill="none" stroke="{TEAL}" stroke-width="2"/>')
	b.append(f'<path d="M{zx1:.1f},143 L{x0},170 M{zx2:.1f},143 L{x1},170" stroke="{TEAL}" stroke-opacity="0.35" fill="none"/>')

	# zoom: one minute, 1,800 frames
	b.append(Text(x0, 188, 'ONE MINUTE · 1,800 FRAMES → 45 KEYFRAMES (ONE PER ~20 m TRAVELLED)', 10.5, MUTED, 500, mono=True, spacing=1))
	top, bottom = 198, 262
	b.append(f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" rx="8" fill="{PANEL}" stroke="{BORDER}"/>')
	frames = 1800
	step = (x1 - x0 - 20) / frames
	hover = (1040, 1220)  # frames with zero baseline (hover / turn)
	b.append(f'<rect x="{x0 + 10 + hover[0] * step:.1f}" y="{top + 6}" width="{(hover[1] - hover[0]) * step:.1f}" height="{bottom - top - 12}" fill="{GREY}" fill-opacity="0.35"/>')
	b.append(Text(x0 + 10 + (hover[0] + hover[1]) / 2 * step, bottom - 14, 'hover: no parallax', 10, TEXT, 500, anchor='middle', mono=True))
	for f in range(0, frames, 4):
		x = x0 + 10 + f * step
		b.append(f'<line x1="{x:.1f}" y1="{top + 14}" x2="{x:.1f}" y2="{bottom - 30}" stroke="{FAINT}" stroke-opacity="0.35" stroke-width="1"/>')
	f = 20
	while f < frames:
		if hover[0] <= f <= hover[1]:
			f = hover[1] + 5
			continue
		x = x0 + 10 + f * step
		roll = rng.random()
		if roll < 0.07:
			b.append(f'<rect x="{x - 1.5:.1f}" y="{top + 8}" width="3" height="{bottom - top - 40}" fill="{AMBER}"/>')
			f += 3
			continue
		if roll < 0.10:
			b.append(f'<rect x="{x - 1.5:.1f}" y="{top + 8}" width="3" height="{bottom - top - 40}" fill="{RED}"/>')
			f += 3
			continue
		b.append(f'<rect x="{x - 1.5:.1f}" y="{top + 8}" width="3" height="{bottom - top - 40}" rx="1" fill="{TEAL}"/>')
		f += 40 + rng.randint(-2, 2)

	b.append(f'<rect x="{x0}" y="282" width="{x1 - x0}" height="34" rx="8" fill="{PANEL_2}"/>')
	b.append(Text(x0 + 16, 304, 'keep = sharpness > τ_sharp  ∧  saturated_pixels < τ_glare  ∧  distance_since_last_keyframe ≥ B', 13, TEXT, 500, mono=True))
	b.append(Text(x1 - 16, 304, 'B from GPS at runtime (≈ 20 m)', 12, TEAL, 500, anchor='end', mono=True))
	legend = [(TEAL, 'kept'), (AMBER, 'rejected: blur'), (RED, 'rejected: glare'), (GREY, 'hover / turn: gated out')]
	lx = x0
	for color, label in legend:
		b.append(f'<rect x="{lx}" y="330" width="12" height="12" rx="3" fill="{color}"/>')
		b.append(Text(lx + 18, 341, label, 12, MUTED, 400))
		lx += 30 + len(label) * 7.2
	Write('keyframes.svg', Svg(w, h, '\n'.join(b)))


# ------------------------------------------------------------------ fusion

def Skyline(x0, y0, width, height):
	# simple terrain + buildings silhouette in panel coordinates
	pts = []
	xs = np.linspace(0, 1, 61)
	for t in xs:
		ground = 0.72 + 0.06 * math.sin(t * 5.3) + 0.03 * math.sin(t * 13)
		for bx, bw, bh in [(0.12, 0.1, 0.32), (0.3, 0.07, 0.48), (0.42, 0.12, 0.26), (0.63, 0.08, 0.55), (0.78, 0.1, 0.3)]:
			if bx <= t <= bx + bw:
				ground = min(ground, 0.72 - bh)
		pts.append((x0 + t * width, y0 + ground * height))
	return pts


def Fusion():
	w, h = 1200, 520
	b = [Header('STEP 7 · SCALE ALIGNMENT', 'Complete from the AI. Accurate from the geometry.')]
	pw, ph = 330, 250
	xs = [40, 435, 830]
	titles = [('Monocular depth', 'Track B · Depth Anything V2', CORAL), ('Sparse structure-from-motion', 'Track A · COLMAP + GPS priors', TEAL), ('Scaled dense depth', 'Step 7 output', TEAL)]
	captions = [('Complete: a value for every pixel', 'No real-world scale'), ('Metric: scale from GPS over the flight', 'Full of holes where nothing matched'), ('Complete and metric', 'Every depth map stretched to real metres')]
	rng = random.Random(7)
	for i, x in enumerate(xs):
		title, sub, color = titles[i]
		b.append(f'<rect x="{x}" y="108" width="{pw}" height="{ph + 104}" rx="14" fill="{PANEL}" stroke="{BORDER if i < 2 else TEAL}" stroke-width="{1.5 if i < 2 else 2}"/>')
		b.append(Text(x + 20, 138, title, 15, TEXT, 600))
		b.append(Text(x + 20, 158, sub, 11, color, 500, mono=True))
		pts = Skyline(x + 20, 172, pw - 40, ph - 30)
		poly = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
		base = f'{x + pw - 20},{172 + ph - 30} {x + 20},{172 + ph - 30}'
		gid = f'depth{i}'
		if i == 0:
			b.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CORAL}" stop-opacity="0.85"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0.9"/></linearGradient></defs>')
			b.append(f'<polygon points="{poly} {base}" fill="url(#{gid})"/>')
			b.append(Text(x + pw - 28, 190, '? m', 18, CORAL, 700, anchor='end', mono=True))
		elif i == 1:
			b.append(f'<polyline points="{poly}" fill="none" stroke="{FAINT}" stroke-dasharray="3 6"/>')
			for px, py in pts:
				if rng.random() < 0.55:
					for _ in range(rng.randint(1, 3)):
						b.append(f'<circle cx="{px + rng.uniform(-3, 3):.1f}" cy="{py + rng.uniform(0, 26):.1f}" r="2.4" fill="{TEAL}"/>')
		else:
			b.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.9"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0.9"/></linearGradient></defs>')
			b.append(f'<polygon points="{poly} {base}" fill="url(#{gid})"/>')
			bar_y = 190
			b.append(f'<line x1="{x + pw - 150}" y1="{bar_y}" x2="{x + pw - 30}" y2="{bar_y}" stroke="{TEXT}" stroke-width="2"/>')
			for k in range(4):
				tx = x + pw - 150 + k * 40
				b.append(f'<line x1="{tx}" y1="{bar_y - 5}" x2="{tx}" y2="{bar_y + 5}" stroke="{TEXT}" stroke-width="1.5"/>')
			b.append(Text(x + pw - 90, bar_y - 10, '0 — 30 m', 11, TEXT, 500, anchor='middle', mono=True))
		c1, c2 = captions[i]
		b.append(Text(x + 20, 108 + ph + 60, c1, 13, TEXT, 500))
		b.append(Text(x + 20, 108 + ph + 82, c2, 13, CORAL if i == 0 else (MUTED if i == 1 else TEAL), 500))
	b.append(Text(402, 245, '×', 34, MUTED, 300, anchor='middle'))
	b.append(Text(800, 245, '=', 34, MUTED, 300, anchor='middle'))
	b.append(f'<rect x="40" y="478" width="1120" height="0" fill="none"/>')
	b.append(Text(40, 496, 'Per frame:  minimise Σ ρ( a · d_AI(p) + b − d_sparse(p) )  over sparse points p visible in that frame  ·  robust loss / RANSAC', 12.5, MUTED, 400, mono=True))
	Write('fusion.svg', Svg(w, h, '\n'.join(b)))


# ------------------------------------------------------------------ confidence

def Confidence():
	w, h = 1200, 500
	b = [Header('CONFIDENCE MODEL', 'Every surface says how it was obtained')]
	cx, cy, s = 372, 300, 25
	c30 = math.cos(math.radians(30))

	def Iso(x, y, z):
		return (cx + (x - y) * c30 * s, cy + (x + y) * 0.5 * s - z * s)

	def Poly(points, fill, stroke, width=1.2, extra=''):
		pts = ' '.join(f'{px:.1f},{py:.1f}' for px, py in (Iso(*p) for p in points))
		return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

	# external base terrain, then the reconstructed corridor
	b.append(Poly([(-6.5, -6.5, 0), (6.5, -6.5, 0), (6.5, 6.5, 0), (-6.5, 6.5, 0)], GREY, '#7D8996', 1, 'fill-opacity="0.35"'))
	b.append(Poly([(-6.5, -2.2, 0), (6.5, -2.2, 0), (6.5, 6.4, 0), (-6.5, 6.4, 0)], TEAL_D, TEAL, 1, 'fill-opacity="0.35" stroke-opacity="0.6"'))
	for k in range(-6, 7):
		a1, a2 = Iso(k, -6.5, 0), Iso(k, 6.5, 0)
		b.append(f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}" stroke="{BG}" stroke-opacity="0.25"/>')
		a1, a2 = Iso(-6.5, k, 0), Iso(6.5, k, 0)
		b.append(f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}" stroke="{BG}" stroke-opacity="0.25"/>')

	x0, x1, y0, y1, z = -1.4, 1.4, -1.0, 1.2, 2.6
	# hidden back walls (inferred), drawn dashed
	back = [(x0, y0, 0), (x1, y0, 0), (x1, y0, z), (x0, y0, z)]
	b.append(Poly(back, 'none', CORAL, 1.4, 'stroke-dasharray="5 5"'))
	b.append(Poly([(x0, y0, 0), (x0, y1, 0), (x0, y1, z), (x0, y0, z)], 'none', CORAL, 1.4, 'stroke-dasharray="5 5"'))
	# right wall faces +x: never seen by the drone -> inferred (extruded)
	b.append(Poly([(x1, y0, 0), (x1, y1, 0), (x1, y1, z), (x1, y0, z)], 'url(#hatch)', CORAL, 1.8))
	# front wall faces +y toward the flight line -> measured
	b.append(Poly([(x0, y1, 0), (x1, y1, 0), (x1, y1, z), (x0, y1, z)], TEAL, TEAL, 1.8, 'fill-opacity="0.75"'))
	# roof -> measured
	b.append(Poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], TEAL, TEAL, 1.8, 'fill-opacity="0.95"'))

	# the single flight line on the measured side, with camera frustums
	fy, fz = 5.6, 2.6
	p1, p2 = Iso(-6.0, fy, fz), Iso(6.0, fy, fz)
	b.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{AMBER}" stroke-width="2.2" stroke-dasharray="9 7"/>')
	# camera positions along the line and their sight lines onto the faces they can see
	roof_c = Iso(0, 0.1, z)
	front_c = Iso(0, y1, z * 0.5)
	for k in (-4.5, -2.0, 0.5, 3.0):
		cam = Iso(k, fy, fz)
		for target in (roof_c, front_c):
			b.append(f'<line x1="{cam[0]:.1f}" y1="{cam[1]:.1f}" x2="{target[0]:.1f}" y2="{target[1]:.1f}" stroke="{TEAL}" stroke-opacity="0.45" stroke-width="1.1"/>')
	for k in (-4.5, -2.0, 0.5, 3.0):
		cam = Iso(k, fy, fz)
		b.append(f'<circle cx="{cam[0]:.1f}" cy="{cam[1]:.1f}" r="5.5" fill="{BG}" stroke="{AMBER}" stroke-width="2"/>')
	lab = Iso(-6.0, fy, fz)
	b.append(Text(lab[0] - 6, lab[1] - 12, 'single flight line', 11, AMBER, 500, mono=True))

	# legend
	lx = 760
	items = [
		(TEAL, 'Measured', ['Seen from two or more viewpoints with a', 'good triangulation angle. The ≤ 1 m claim', 'applies here.']),
		(CORAL, 'Inferred', ['AI depth with no geometric backing, or walls', 'extruded from the roof outline. Plausible,', 'unverified — measurements across it warn.']),
		(GREY, 'External', ['Base terrain (SRTM / Cesium World Terrain).', '5–16 m vertical, historical — context only,', 'never blended into the reconstruction.']),
	]
	for i, (color, name, lines) in enumerate(items):
		y = 130 + i * 112
		fill = 'url(#hatch)' if name == 'Inferred' else color
		b.append(f'<rect x="{lx}" y="{y}" width="28" height="28" rx="6" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
		b.append(Text(lx + 44, y + 20, name, 17, TEXT, 600))
		for j, line in enumerate(lines):
			b.append(Text(lx + 44, y + 44 + j * 18, line, 12.5, MUTED, 400))
	b.append(Text(40, 476, 'Confidence per voxel = views that saw it × max triangulation angle × source (triangulated vs prior). It drives measurement error bars, the coverage-gap map and the re-fly advisor.', 12.5, MUTED, 400))
	Write('confidence.svg', Svg(w, h, '\n'.join(b)))


# ------------------------------------------------------------------ timing

def Timing():
	w, h = 1200, 330
	b = [Header('TIMING BUDGET', '< 15 minutes for a 10-minute flight — design estimate on a decent GPU')]
	stages = [
		('Decode + keyframes', 150, TEAL_D),
		('SuperPoint', 15, TEAL),
		('Matching + bundle adjustment', 330, TEAL_D),
		('SegFormer', 15, CORAL),
		('Depth', 20, CORAL),
		('Scale', 10, TEAL),
		('TSDF fusion', 90, TEAL_D),
		('Mesh + buildings + texture', 150, TEAL),
		('Export', 60, TEAL_D),
	]
	x0, scale = 40, 1.12
	y = 150
	x = x0
	for i, (name, sec, color) in enumerate(stages):
		width = sec * scale
		b.append(f'<rect x="{x:.1f}" y="{y}" width="{width - 2:.1f}" height="40" rx="5" fill="{color}" fill-opacity="{0.9 if i % 2 == 0 else 0.7}"/>')
		if width > 60:
			b.append(Text(x + 8, y + 25, name, 12, '#FFFFFF', 600))
			b.append(Text(x + 8, y + 60, f'~{sec // 60} min {sec % 60:02d} s' if sec >= 60 else f'~{sec} s', 11, MUTED, 400, mono=True))
		x += width
	total = sum(s for _, s, _ in stages)
	small = [('SuperPoint', 15), ('SegFormer', 15), ('Depth', 20), ('Scale', 10)]
	b.append(Text(x0, 250, 'Short stages: SuperPoint ~15 s · SegFormer ~15 s · Depth Anything V2 ~20 s · scale alignment ~10 s', 11.5, MUTED, 400, mono=True))
	budget_x = x0 + 900 * scale
	b.append(f'<line x1="{budget_x:.1f}" y1="118" x2="{budget_x:.1f}" y2="226" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>')
	b.append(Text(budget_x + 6, 128, '900 s budget', 11.5, RED, 600, mono=True))
	b.append(Text(x0, 132, f'≈ {total // 60} min total, sequential', 12, TEXT, 600))
	# in-flight span: steps 1-6
	in_flight = (150 + 15 + 330 + 15 + 20) * scale
	b.append(f'<path d="M{x0},276 L{x0},284 L{x0 + in_flight:.1f},284 L{x0 + in_flight:.1f},276" fill="none" stroke="{AMBER}" stroke-width="1.8"/>')
	b.append(Text(x0 + 8, 302, 'steps 1–6 stream during the flight', 12, AMBER, 600, mono=True))
	after = (10 + 90 + 150 + 60) * scale
	b.append(f'<path d="M{x0 + in_flight + 4:.1f},276 L{x0 + in_flight + 4:.1f},284 L{x0 + in_flight + 4 + after:.1f},284 L{x0 + in_flight + 4 + after:.1f},276" fill="none" stroke="{TEAL}" stroke-width="1.8"/>')
	b.append(Text(x0 + in_flight + 12, 302, '≈ 5 min after landing', 12, TEAL, 600, mono=True))
	Write('timing.svg', Svg(w, h, '\n'.join(b)))


# ------------------------------------------------------------------ banner

def Banner(logo_path):
	W, H = 1600, 520
	img = Image.new('RGB', (W, H), '#08253F')
	yy, xx = np.mgrid[0:H, 0:W]
	d = np.sqrt(((xx - W * 0.72) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 1.1)) ** 2)
	t = np.clip(d, 0, 1)[..., None]
	c0 = np.array([22, 80, 124], dtype=np.float32)
	c1 = np.array([7, 26, 44], dtype=np.float32)
	img = Image.fromarray((c0 * (1 - t) + c1 * t).astype(np.uint8), 'RGB')

	# dotted terrain seen in perspective, a single flight line with camera frustums above it
	layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
	draw = ImageDraw.Draw(layer)
	rng = np.random.default_rng(158)
	horizon, cam_h, fov = 170, 1.0, 900
	for row in range(1, 70):
		z = 1.0 + row * 0.28
		for col in range(-90, 91):
			xw = col * 0.14
			height = 0.10 * math.sin(xw * 1.3 + z * 0.6) + 0.06 * math.sin(xw * 3.1 - z) + 0.25 * math.exp(-((xw - 1.6) ** 2 + (z - 6.5) ** 2) / 1.5)
			sx = W * 0.7 + xw / z * fov
			sy = horizon + (cam_h - height) / z * fov * 0.55
			if not (W * 0.36 < sx < W + 10 and horizon < sy < H + 10):
				continue
			near = max(0.0, 1 - row / 70)
			r = 0.8 + 2.4 * near
			a = int(40 + 175 * near)
			lift = min(1, height * 3.5)
			color = (int(63 + 150 * lift), int(179 + 50 * lift), int(207 + 30 * lift), a)
			draw.ellipse((sx - r, sy - r, sx + r, sy + r), fill=color)
	# flight line
	fx0, fx1, fy = int(W * 0.40), W - 40, 118
	for x in range(fx0, fx1, 26):
		draw.line((x, fy, x + 14, fy), fill=(245, 179, 66, 220), width=3)
	for k in range(7):
		x = fx0 + 60 + k * (fx1 - fx0 - 120) / 6
		draw.polygon([(x, fy + 4), (x - 16, fy + 34), (x + 16, fy + 34)], fill=(245, 179, 66, 60), outline=(245, 179, 66, 220))
	layer = layer.filter(ImageFilter.GaussianBlur(0.4))
	img = Image.alpha_composite(img.convert('RGBA'), layer)

	# left fade for legibility
	fade = Image.new('L', (W, H))
	fd = ImageDraw.Draw(fade)
	for x in range(W):
		v = int(max(0, min(1, (W * 0.58 - x) / (W * 0.22))) * 200)
		fd.line((x, 0, x, H), fill=v)
	dark = Image.new('RGBA', (W, H), (8, 30, 50, 255))
	img = Image.composite(dark, img, fade)

	logo = Image.open(logo_path).convert('RGBA')
	lh = 128
	logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
	img.alpha_composite(logo, (110, 150))
	draw = ImageDraw.Draw(img)
	mono = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 19)
	light = ImageFont.truetype('C:/Windows/Fonts/segoeuil.ttf', 50)
	regular = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 24)
	draw.text((114, 104), 'SIH 2026  ·  PS SIH26158  ·  TEAM HONEYBADGER', font=mono, fill=(63, 179, 207))
	draw.text((110, 306), 'One pass. Full picture.', font=light, fill=(240, 246, 250))
	draw.text((112, 380), 'Single-pass drone video  →  georeferenced, metrically accurate 3D', font=regular, fill=(160, 180, 198))
	draw.text((112, 414), 'that tells you what it measured, what it inferred and what it could not see.', font=regular, fill=(160, 180, 198))
	img.convert('RGB').save(os.path.join(HERE, 'banner.png'), optimize=True)
	print('wrote banner.png')


if __name__ == '__main__':
	import sys
	Pipeline()
	Baseline()
	Keyframes()
	Fusion()
	Confidence()
	Timing()
	Banner(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'scout_logo_dark.png'))
