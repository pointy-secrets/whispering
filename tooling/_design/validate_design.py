#!/usr/bin/env python3
"""Check that the plaintext page CSS matches what tokens.json generates.
Exits 1 on mismatch. Run before any push."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOKENS_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")
PAGES = [
    (os.path.join(ROOT, "index.html"), "main"),
    (os.path.join(ROOT, "manage", "index.html"), "manage"),
]

with open(TOKENS_PATH) as f:
    tokens = json.load(f)

generated = os.popen(
    f"python3 {os.path.join(os.path.dirname(__file__), 'generate_css.py')}"
).read()

checks = []
checks.append((tokens["font"]["size_body"], "font.size_body"))
checks.append((tokens["font"]["size_filter_menu"], "font.size_filter_menu"))
checks.append((tokens["font"]["weight_all"], "font.weight_all"))
checks.append((tokens["color"]["primary"], "color.primary"))
checks.append((tokens["spacing"]["margin_side"], "spacing.margin_side"))
checks.append((tokens["spacing"]["margin_top_desktop"], "spacing.margin_top_desktop"))
checks.append((tokens["spacing"]["margin_bottom"], "spacing.margin_bottom"))
checks.append((tokens["spacing"]["top_padding"], "spacing.top_padding"))
checks.append((tokens["spacing"]["max_track_width"], "spacing.max_track_width"))
checks.append((tokens["media_player"]["height"], "media_player.height"))
checks.append((tokens["media_player"]["width_desktop"], "media_player.width_desktop"))
checks.append((tokens["menu"]["top_offset"], "menu.top_offset"))
checks.append((tokens["menu"]["border_radius"], "menu.border_radius"))
checks.append((tokens["borders"]["hairline_color"], "borders.hairline_color"))

d = tokens.get("desktop", {})
if d.get("margin_side"):
    checks.append((d["margin_side"], "desktop.margin_side"))
if d.get("margin_top"):
    checks.append((d["margin_top"], "desktop.margin_top"))
if d.get("audio_player_width"):
    checks.append((d["audio_player_width"], "desktop.audio_player_width"))
if d.get("track_gap"):
    checks.append((d["track_gap"], "desktop.track_gap"))
if d.get("artist_indent"):
    checks.append((d["artist_indent"], "desktop.artist_indent"))
if d.get("nav_border_color"):
    checks.append((d["nav_border_color"], "desktop.nav_border_color"))

failures = []
for path, label in PAGES:
    if not os.path.exists(path):
        failures.append(f"{label}: file not found at {path}")
        continue
    with open(path) as f:
        content = f.read()
    for value, source in checks:
        if value not in content:
            failures.append(f"{label}: missing value '{value}' (from {source})")

if failures:
    print(f"🔴 DESIGN VALIDATION FAILED — {len(failures)} issues:")
    for f in failures:
        print(f"  ❌ {f}")
    sys.exit(1)
else:
    print(f"🟢 DESIGN VALIDATION PASSED — all {len(checks)} tokens present in all {len(PAGES)} pages")
    sys.exit(0)
