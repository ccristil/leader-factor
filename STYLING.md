# LeaderFactor — Styling Reference

Extracted from the live site's canonical design-token stylesheet
(`leaderfactor.com/styles/lf-tokens.css`, "Colors & Type v2.0", dated 2026-05-29)
plus `site.css`. This is the real system the marketing site uses, not an
approximation. Use it to make this prototype look like it belongs to LeaderFactor.

**The one-line summary:** cream/warm-sand light UI, near-black ink, one accent
sand tone, **fully-pill buttons**, **flat cards with 16px radius and no shadows**,
two typefaces only (Fustat sans + Spectral italic serif accent), and a fast
`0.18s ease` on everything. Restrained and editorial, not flashy.

---

## Typefaces

Two faces, only two.

| Role | Family | Notes |
|------|--------|-------|
| Sans (everything) | **Fustat** | Self-hosted variable font, weights 200–800. Fallback: `system-ui, -apple-system, 'Segoe UI', sans-serif` |
| Serif accent | **Spectral**, *italic only* | Google Fonts. Weights 300/400/500. Used for the display headline, one feature word inside a heading, numerals, and step labels — never body copy. |

```css
--font-sans:  'Fustat', system-ui, -apple-system, 'Segoe UI', sans-serif;
--font-serif: 'Spectral', Georgia, 'Times New Roman', serif;
```

Fustat is brand-licensed. For a prototype, either self-host the TTFs from
`leaderfactor.com/styles/fonts/Fustat-VariableFont_wght.ttf` or fall back to
`system-ui`. Spectral is free on Google Fonts:

```css
@import url('https://fonts.googleapis.com/css2?family=Spectral:ital,wght@1,300;1,400;1,500&display=swap');
```

---

## Type scale

Size / line-height / letter-spacing. Body default is `p2` (16px / 1.4).

| Token | Size | Line-height | Letter-spacing | Weight | Face |
|-------|------|-------------|----------------|--------|------|
| display | 158px | 1.06 | −0.04em | 300 | **Spectral italic** |
| h1 | 64px | 1.1 | 0 | 400 | Fustat |
| h2 | 40px | 1.2 | 0 | 400 | Fustat |
| h3 | 32px | 1.2 | 0 | 400 | Fustat |
| h4 | 20px | 1.0 | 0.01em | 700 | Fustat |
| h5 | 18px | 1.35 | 0 | 500 | Fustat |
| lead | 25px | 1.1 | — | 500 | Fustat |
| p1 | 20px | 1.35 | — | 400 | Fustat |
| p2 (body) | 16px | 1.4 | — | 400 | Fustat |
| p3 (small) | 13px | 1.4 | — | 400 | Fustat |
| step | 28px | — | −0.02em | 400 | Spectral italic |

Note the low heading weights: h1–h3 are **regular (400)**, not bold. Only h4 is
bold. Headings read light and editorial.

**Serif accent usage:** `.lf-accent` / `.lf-numeral` — Spectral italic 400,
`letter-spacing: -0.02em`. Drop it on one word in a heading or on numerals for
the signature LeaderFactor look.

---

## Color palette

### Neutrals / surfaces (the workhorses)

| Token | Hex | Use |
|-------|-----|-----|
| `--lf-cream` | `#FFFEF8` | **Page background (light mode)** |
| `--lf-white` | `#FFFFFF` | Elevated surfaces (cards) |
| `--lf-sand-10` | `#F7F3EA` | Sunken / lightest beige card bg |
| `--lf-sand-30` | `#E7DDCE` | Card backgrounds on cream |
| `--lf-dark` | `#101322` | **Primary ink / body text; the "black"** |
| `--lf-navy` | `#081238` | Deep backgrounds, gradient floor |
| `--lf-midnight` | `#02071C` | Glass tint base |

### Mid greys (text + lines)

| Token | Hex | Use |
|-------|-----|-----|
| `--lf-md-90` | `#353949` | Dark elevated surfaces |
| `--lf-md-70` | `#4E5160` | Body copy on light (muted text) |
| `--lf-md-50` | `#80838D` | Secondary / faded text |
| `--lf-md-30` | `#B3B5BB` | Dividers, disabled |
| `--lf-md-10` | `#E6E6E8` | Light dividers on cream |

### Sand scale (the signature warm tone)

`#F7F3EA` → `#E7DDCE` → `#D7C7B1` → `#C7B095` → **`#AF8F6B` (`--lf-sand`, signature)** → `#7F5D37` → `#543615`

`--lf-sand #AF8F6B` is the default warm accent. It's also the "AI Leadership"
solution color.

### Brand accents (use alone, never mixed with a solution color)

| Token | Hex |
|-------|-----|
| `--lf-plum` | `#802B64` |
| `--lf-plum-bright` | `#A43178` |
| `--lf-accent-blue` | `#066DB1` |
| `--lf-accent-blue-bright` | `#0C81CF` |

### Solution color scales

Each product/solution has a 5-step scale: `default / bright / tint-30 / shade-120 / deep-150`.
There's an **active-solution slot** (`--solution`, `--solution-bright`, …) that
defaults to PS (blue) and gets remapped by adding a class (`.is-ps`, `.is-eq`,
`.is-cam`, `.is-epic`, `.is-dm`, `.is-ltai`, `.is-tp`) on a subtree.

| Code | Name (inferred) | default | bright | tint-30 | shade-120 | deep-150 |
|------|-----------------|---------|--------|---------|-----------|----------|
| ps | Psychological Safety | `#2A77EA` | `#0268FF` | `#B4CCF0` | `#225BB0` | `#072F6A` |
| eq | (green) | `#659940` | `#62AE2C` | `#CBE2BB` | `#4E7333` | `#2F4D1A` |
| cam | (orange/red) | `#F04624` | `#FF4823` | `#FEB1A1` | `#D84022` | `#902A16` |
| epic | (cyan) | `#43A9C2` | `#30C3E8` | `#BAE5F0` | `#347E91` | `#104957` |
| dm | (purple) | `#6B49DB` | `#774EFF` | `#C9BAFB` | `#5B3DBE` | `#3E2B7D` |
| ltai | AI Leadership (sand) | `#AF8F6B` | `#C7B095` | `#E7DDCE` | `#7F5D37` | `#543615` |
| tp | (lime) | `#B2C600` | `#C8D92B` | `#DEE69B` | `#94A500` | `#5B6500` |

For this take-home, pick **one** solution accent to theme dashboards/metrics
(PS blue `#2A77EA` or the sand `#AF8F6B` are the safest brand-forward choices).

---

## Semantic tokens (build against these, not raw hex)

Light mode is the default. `[data-theme="dark"]` remaps them.

| Token | Light | Dark |
|-------|-------|------|
| `--bg` | `#FFFEF8` cream | `#101322` |
| `--bg-elevated` | `#FFFFFF` | `#1B2032` |
| `--bg-sunken` | `#F7F3EA` sand-10 | `#02071C` |
| `--fg` | `#101322` | `#FFFFFF` |
| `--fg-muted` | `#4E5160` | `rgba(255,255,255,.70)` |
| `--fg-subtle` | `#6A6D78` | `rgba(255,255,255,.50)` |
| `--fg-faint` | `#B3B5BB` | `rgba(255,255,255,.30)` |
| `--border` | `#E6E6E8` | `rgba(255,255,255,.10)` |
| `--line` | `#E6E6E8` | `rgba(255,255,255,.15)` |

**Text-on-dark helpers:** white / `rgba(255,255,255,.70)` body / `.50` subtle / `.30` faint.

---

## Corner radii

| Token | Value | Use |
|-------|-------|-----|
| `--radius-pill` | `2000px` | **Buttons — always fully pill** |
| `--radius-card` | `16px` | Cards |
| `--radius-hero` | `10px` | Large hero containers / inset canvas |
| `--radius-chip` | `5px` | Dropdowns, chips |
| `--radius-navbar` | `0 0 5px 5px` | Navbar bottom corners only |

---

## Shadows

**LeaderFactor uses almost none. Cards are flat.** Do not add drop shadows to
cards. The only shadow in the system is for cards floating over the hero image:

```css
--shadow-float: 0 30px 80px -40px rgba(2, 7, 28, 0.35);
```

---

## Spacing & layout

4-based scale:

| Token | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| px | 4 | 8 | 12 | 16 | 24 | 36 | 48 | 72 | 96 | 144 |

```css
--max-width: 1200px;
--gutter: 150px;
--section-pad: 96px;   /* vertical rhythm between sections */
```

---

## Motion

One transition, used for opacity / transform / background-color only:

```css
--transition: 0.18s ease;
```

Fast and subtle. Don't invent bouncy/long animations.

---

## Components

### Buttons — always fully pill, 48px tall

```css
.lf-button {
  display: inline-flex; align-items: center; justify-content: center; gap: 10px;
  height: 48px; padding: 0 28px;
  font: 500 13px/1 'Fustat', sans-serif;   /* p3, weight 500 */
  color: #FFFFFF;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 2000px;                    /* pill */
  background: rgba(2,7,28,0.12);
  backdrop-filter: blur(20px) saturate(140%);
  transition: background .18s ease, border-color .18s ease, transform .18s ease;
}
.lf-button:hover  { background: rgba(255,255,255,0.18); border-color: rgba(255,255,255,0.22); }
.lf-button:active { background: #FFFFFF; color: #101322; transform: translateY(1px); }
```

Variants:
- `.lf-button--on-light` — for light backgrounds: `background: rgba(16,19,34,0.05)`, dark text, no blur. Hover darkens the tint; active inverts to dark bg / white text.
- `.lf-button--solid` — dark solid: `background: #101322`, white text. Hover `#1B2032`; active inverts to white bg / dark text.

Note the signature **active-state inversion** (fill flips to white, text to dark).

### Arrow link — underline on hover only

```css
.lf-arrow-link { display: inline-flex; align-items: center; gap: 6px;
  color: currentColor; text-decoration: none; }
.lf-arrow-link:hover { text-decoration: underline; }
.lf-arrow-link svg { width: 18px; height: 18px; }
```

### Cards — flat, 16px, bordered, no shadow

```css
.lf-card {
  background: var(--bg-elevated);   /* #FFFFFF light */
  border: 1px solid var(--border);  /* #E6E6E8 light */
  border-radius: 16px;
}
```

### Dot-title (all-caps overline with a square bullet)

The recurring section-label style: uppercase, 12px, `letter-spacing: 0.1em`,
weight 500, preceded by a small **square** (not round) bullet in `currentColor`.

```css
.lf-dot-title {
  display: inline-flex; align-items: center; gap: 8px;
  font: 500 12px/1.2 'Fustat'; text-transform: uppercase; letter-spacing: 0.1em;
}
.lf-dot-title::before { content:""; width:7px; height:7px; border-radius:0; background: currentColor; }
```

---

## Backgrounds & effects

- `.lf-bg-light` → cream `#FFFEF8`; `.lf-bg-dark` → `#101322`.
- **Page-top hero gradient:** `linear-gradient(180deg, #081238 navy 0%, #AF8F6B sand 55%, #FFFEF8 cream 100%)`.
- **Glass:** always pair a translucent fill with `backdrop-filter: blur()`.
  Tints: `--glass-dark rgba(2,7,28,.25)`, `--glass-light rgba(255,255,255,.15)`.
  Blur presets: glass 12px, navbar 28px, overlay 64px.
- **Dot-grid overlay:** `radial-gradient(rgba(255,255,255,.10) 1px, transparent 1px)` at `24px 24px`.
- Hero scrim over photos: `rgba(16,19,34,0.51)`.

---

## Practical defaults for this prototype

Since this is an admin/manager/learner dashboard, not a marketing page, lean on
the calm end of the system:

- **Background** `#FFFEF8` cream, **ink** `#101322`, **muted text** `#4E5160`.
- **Cards:** white, `1px solid #E6E6E8`, `16px` radius, **no shadow**.
- **Buttons:** pill, `.lf-button--solid` (dark) for primary, `.lf-button--on-light` for secondary.
- **One accent** for charts/highlights/status — PS blue `#2A77EA` or sand `#AF8F6B`.
- **Section labels:** the `.lf-dot-title` uppercase-with-square-bullet pattern.
- **Headings light (400 weight)**, Fustat. Sprinkle one **Spectral italic** accent word or use it for big numerals in metrics.
- Transitions `0.18s ease`. Spacing on the 4/8/16/24/36/48/72/96 scale.

### Minimal `:root` to drop into the app

```css
:root {
  --bg:#FFFEF8; --bg-elevated:#FFFFFF; --bg-sunken:#F7F3EA;
  --fg:#101322; --fg-muted:#4E5160; --fg-subtle:#6A6D78; --fg-faint:#B3B5BB;
  --border:#E6E6E8;
  --accent:#2A77EA;            /* or sand #AF8F6B */
  --font-sans:'Fustat',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-serif:'Spectral',Georgia,serif;
  --radius-card:16px; --radius-pill:2000px; --radius-chip:5px;
  --transition:0.18s ease;
}
```
