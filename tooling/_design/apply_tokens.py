#!/usr/bin/env python3
"""Apply tokens.json CSS to all three pages. Idempotent — safe to run multiple times."""
import re, sys, os

TOKENS_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")
PAGES = [
    "/root/new-index.html",
    "/root/upload-form-plain.html",
    "/root/manage-form-plain.html",
]

# Generate the full CSS block from tokens
generated_css = os.popen("python3 /root/_design/generate_css.py").read()

# Wrap in <style> tags
style_block = f"<style>\n{generated_css}</style>"

for path in PAGES:
    if not os.path.exists(path):
        print(f"⚠️  {path} not found, skipping")
        continue

    with open(path) as f:
        content = f.read()

    # Replace existing <style>...</style> block
    new_content = re.sub(
        r'<style>.*?</style>',
        style_block,
        content,
        count=1,
        flags=re.DOTALL
    )

    if new_content == content:
        # No <style> block found — insert after <head>
        new_content = content.replace("<head>", f"<head>\n{style_block}")

    with open(path, 'w') as f:
        f.write(new_content)

    print(f"✅ {os.path.basename(path)} — CSS updated")

print("\nDone. Run `python3 _design/validate_design.py` to verify all consistent.")
