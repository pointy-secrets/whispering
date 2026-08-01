#!/usr/bin/env python3
"""Apply tokens.json CSS to the plaintext pages. Idempotent — safe to run multiple times.

Only <style> blocks marked with the generated sentinel are replaced; page-specific
override blocks (no sentinel, e.g. manage/ and home-page overrides) survive.
"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOKENS_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")
PAGES = [
    os.path.join(ROOT, "index.html"),
    os.path.join(ROOT, "manage", "index.html"),
]
SENTINEL = "WHISPERING-GENERATED"

generated_css = os.popen(
    f"python3 {os.path.join(os.path.dirname(__file__), 'generate_css.py')}"
).read().strip()

style_block = (
    f"<style>\n/* {SENTINEL} — do not hand-edit; edit tooling/_design/tokens.json instead */\n"
    f"{generated_css}\n</style>"
)

for path in PAGES:
    if not os.path.exists(path):
        print(f"⚠️  {path} not found, skipping")
        continue

    with open(path) as f:
        content = f.read()

    # Drop previously generated blocks (identified by the sentinel comment).
    new_content = re.sub(
        r'<style>\s*/\* ' + SENTINEL + r' .*?</style>',
        '',
        content,
        flags=re.DOTALL,
    )

    if new_content == content:
        print(f"ℹ️  {os.path.basename(path)} — no generated block found; inserting after <head>")

    # Insert the fresh generated block right after <head> so page-specific blocks (below) win the cascade.
    new_content = new_content.replace("<head>", f"<head>\n{style_block}", 1)

    with open(path, 'w') as f:
        f.write(new_content)

    print(f"✅ {os.path.basename(path)} — CSS updated")

print("\nDone. Run `python3 tooling/_design/validate_design.py` to verify all consistent.")
