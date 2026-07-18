import json

with open('tokens.json', 'r') as f:
    t = json.load(f)

# Extract tokens
def get_v(path):
    parts = path.split('.')
    cur = t
    for p in parts:
        cur = cur[p]
    return cur.get('$value', 'var(--' + path + ')')

# W3C format is nested; flatten it manually for the CSS
css_vars = [
    f"--color-primary: {get_v('color.primary')};",
    f"--color-ink: rgba({get_v('color.ink')}, 1);",
    f"--color-reverse: rgba({get_v('color.reverse')}, 1);",
    f"--color-background: {get_v('color.background')};",
    f"--color-panel: rgba({get_v('color.panel')}, 1);",
    f"--font-family: {get_v('font.family')};",
    f"--font-weight-base: {get_v('font.weight.base')};",
    f"--font-size-body: {get_v('font.size.body')};",
    f"--font-size-meta: {get_v('font.size.meta')};",
    f"--font-size-display: {get_v('font.size.display')};",
    f"--space-side: {get_v('space.side')};",
    f"--space-side-mobile: {get_v('space.side_mobile')};",
    f"--space-top: {get_v('space.top')};",
    f"--radius-pill: {get_v('radius.pill')};",
    f"--radius-media: {get_v('radius.media')};",
]

base_css = """
body {
  font-family: var(--font-family);
  font-weight: var(--font-weight-base);
  font-size: var(--font-size-body);
  background-color: var(--color-background);
  color: var(--color-ink);
  margin: 0;
  padding: 0;
  line-height: 1.4;
}

a {
  color: inherit;
  text-decoration: none;
  transition: opacity 0.2s ease;
}
a:hover {
  opacity: 0.7;
}

.whisper-title {
  font-size: var(--font-size-display);
  font-weight: var(--font-weight-base);
  text-align: center;
  margin: 0;
  line-height: 1;
  letter-spacing: 0.1em;
}

.cargo-editorial-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-side);
  padding: var(--space-top) var(--space-side);
}

.editorial-block {
  grid-column: span 12;
  position: relative;
}

.block-hero { grid-column: 2 / span 10; text-align: center; }
.block-meta { grid-column: 8 / span 4; font-size: var(--font-size-meta); opacity: 0.6; }
.block-nav { grid-column: 2 / span 6; margin-top: 2rem; }

.whisper-link {
  display: inline-block;
  font-size: var(--font-size-meta);
  border: 1px solid rgba(0,0,0,0.1);
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  margin-right: 10px;
  cursor: pointer;
}
.whisper-link:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.whisper-footer {
  position: fixed;
  bottom: var(--space-side);
  left: var(--space-side);
  font-size: var(--font-size-meta);
  opacity: 0.5;
}

.drop-zone {
  background-color: var(--color-panel);
  border: 2px dashed var(--color-primary);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
}
"""

with open('styles.css', 'w') as f:
    f.write(":root {\n  " + "\n  ".join(css_vars) + "\n}\n")
    f.write(base_css)
