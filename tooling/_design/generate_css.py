#!/usr/bin/env python3
"""Read tokens.json and output standardized CSS block for all whispering pages."""
import json, sys, os

TOKENS_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")
with open(TOKENS_PATH) as f:
    t = json.load(f)

f = t["font"]
c = t["color"]
s = t["spacing"]
mp = t["media_player"]
h = t["header"]
m = t["menu"]
b = t["borders"]
mpg = t["manage_page"]
d = t.get("desktop", {})

CSS = f"""@import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap');

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  background: {c['background']};
  color: {c['primary']};
  font-family: {f['family']};
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
  line-height: 1.5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: {s['margin_top_desktop']} {s['margin_side']} {s['margin_bottom']};
}}

a {{ color: {c['primary']}; text-decoration: none; }}
a:hover {{ opacity: 0.7; }}

.container {{
  width: 100%;
  position: relative;
}}

.header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: {s['gap_header_bottom']};
  position: relative;
}}

.header .logo {{
  font-size: {f['size_logo']};
  font-style: {h['logo_style']};
  font-weight: {h['logo_weight']};
  color: {c['primary']};
}}

/* Full-width hairline under the whispering! logo */
.logo-rule {{
  width: 100%;
  border: none;
  border-top: {b['hairline_width']} solid {b['hairline_color']};
  margin: {s['gap_header_bottom']} 0 0;
}}

.filter-btn {{
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 0;
}}
.filter-btn span {{
  display: block;
  width: 18px;
  height: 1px;
  background: {c['primary']};
  border-radius: 1px;
}}

.filter-menu {{
  display: none;
  position: absolute;
  top: {m['top_offset']};
  right: 0;
  background: {c['background']};
  border: 1px solid {c['primary']};
  border-radius: {m['border_radius']};
  min-width: 160px;
  padding: 6px;
  z-index: 10;
}}
.filter-menu.open {{ display: block; }}
.filter-menu button {{
  display: block;
  width: 100%;
  text-align: left;
  padding: {m['item_padding']};
  font-family: {f['family']};
  font-size: {m['item_font_size']};
  font-weight: {f['weight_all']};
  border: none;
  background: none;
  color: {c['primary']};
  cursor: pointer;
  border-radius: 4px;
}}
.filter-menu button:hover {{ background: #f0fafc; }}
.filter-menu button.active {{ color: {c['primary']}; }}
.filter-menu .divider {{
  border-bottom: 0.5px solid {c['primary']};
  margin-bottom: 4px;
  padding-bottom: 8px;
}}
.filter-menu .artist-item {{
  padding-left: {m.get('artist_indent', '16px')};
}}

.track-list {{
  display: flex;
  flex-direction: column;
  gap: {s['gap_tracks']};
  padding-top: {s['top_padding']};
}}

.track {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}

.track audio {{
  width: {mp['width_desktop']};
  max-width: 100%;
  height: {mp['height']};
}}

.track-info {{
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-left: 10px;
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
  color: {c['primary']};
}}
.track-title {{ font-weight: {f['weight_all']}; }}
.track-artist {{ opacity: {c['opacity_muted']}; font-weight: {f['weight_all']}; }}

.form-group {{ margin-bottom: 16px; }}
.form-group label {{
  display: block;
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
  margin-bottom: 6px;
}}
.form-group input[type="text"] {{
  width: 100%;
  padding: 8px 10px;
  border: 1px solid {c['primary']};
  border-radius: 6px;
  font-family: {f['family']};
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
  color: {c['primary']};
  background: {c['background']};
}}
.form-group input::placeholder {{ color: {c['primary']}; opacity: 0.5; }}

.drop-zone {{
  border: 1px solid {c['primary']};
  border-radius: {s['drop_zone_radius']};
  height: {s['drop_zone_height']};
  text-align: center;
  cursor: pointer;
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
}}
.drop-zone .small-text {{
  font-size: 9pt;
  opacity: 0.6;
}}
.drop-zone.dragover {{ background: #f0fafc; }}

button.submit-btn {{
  width: 100%;
  padding: 10px;
  background: {c['primary']};
  color: {c['background']};
  border: none;
  border-radius: 6px;
  font-family: {f['family']};
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
  cursor: pointer;
}}
button.submit-btn:hover {{ opacity: 0.85; }}
button.submit-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}

.status {{ margin-top: 12px; font-size: {f['size_body']}; font-weight: {f['weight_all']}; }}

.title-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}}
.page-title {{ font-size: {f['size_body']}; font-weight: {f['weight_all']}; opacity: {c['opacity_muted']}; }}
select.filter-select {{
  font-family: {f['family']};
  font-size: {m['item_font_size']};
  font-weight: {f['weight_all']};
  color: {c['primary']};
  background: {c['background']};
  border: 1px solid {c['primary']};
  border-radius: 6px;
  padding: 4px 8px;
}}

.hairline {{ border: none; border-top: {b['hairline_width']} solid {b['hairline_color']}; margin: 12px 0; }}

.song-list {{ display: flex; flex-direction: column; gap: 10px; }}
.song-item {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-size: {f['size_body']};
  font-weight: {f['weight_all']};
}}
.song-meta {{ opacity: {c['opacity_muted']}; }}
.delete-btn {{
  background: none;
  border: none;
  cursor: pointer;
  font-family: {f['family']};
  font-size: {mpg['delete_btn_size']};
  font-weight: {f['weight_all']};
  color: {c['primary']};
  padding: 2px 6px;
}}
.delete-btn:hover {{ opacity: 0.6; }}

.back-link {{ margin-top: 16px; font-size: {f['size_body']}; font-weight: {f['weight_all']}; }}

/* ===== DESKTOP-ONLY OVERRIDES (min-width: 601px) ===== */
@media (min-width: 601px) {{
  body {{
    padding: {d.get('margin_top', '24px')} {d.get('margin_side', '80px')} {s['margin_bottom']};
  }}
  .track audio {{
    width: {d.get('audio_player_width', '400px')};
  }}
  .track-list {{
    gap: {d.get('track_gap', '16px')};
  }}
  /* Square drop zone on desktop */
  .drop-zone {{
    aspect-ratio: {d.get('drop_zone_aspect', '1 / 1')};
    height: auto;
    max-width: 400px;
  }}
  /* Scale fonts up on desktop */
  body, .header .logo, .filter-menu button, .track-info, .form-group label,
  .form-group input[type="text"], .status, .page-title, select.filter-select,
  .song-item, .delete-btn, .back-link, .drop-zone, .drop-zone .small-text {{
    font-size: calc({f['size_body']} * {d.get('font_scale', '2')});
  }}
}}

@media (max-width: 600px) {{
  body {{ padding: {s['margin_top_mobile']} {s['margin_side_mobile']} {s['margin_bottom']}; }}
  .container {{ max-width: 100%; }}
  .header .logo {{ font-size: {f['size_logo_mobile']}; }}
}}
@media (min-width: 1200px) {{
  body {{ padding: {s['margin_top_wide']} {s['margin_side']} {s['margin_bottom']}; }}
}}
"""

print(CSS)
