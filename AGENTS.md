# Whispering — AGENTS.md

Pure static site (vanilla HTML/JS/CSS, no build step, no server). Deployed on GitHub Pages at `whispering.living` (CNAME). Repo: `pointy-secrets/whispering`.

## Repository map

| Path | Status | Purpose |
|---|---|---|
| `index.html` | tracked | Main player |
| `upload/index.html` | tracked | Staticrypt-encrypted upload form |
| `manage/index.html` | tracked | Delete songs |
| `template.html` | tracked | Staticrypt re-encryption template |
| `_data/songs.json` | tracked | Song list |
| `audio/`, `assets/uploads/` | tracked | Media files |
| `tooling/` | tracked | Guardrails, design-token pipeline, hooks |
| `.github/workflows/guardrails.yml` | tracked | CI guardrails on push/PR |
| `AGENTS.md` | tracked | This file |
| `.opencode/` | gitignored | Local opencode config + agents (auditor/coder/researcher) + empty scaffold dirs |
| `opencode.json`, `mcp-servers.yaml.txt`, `projects/` | gitignored | Local MCP/inference config, references `/code-projects/...` VM paths |
| `git/hooks/pre-push.sh` | gitignored/untracked | Calls `/code-projects/operating-system/guardrails.sh` — VM path, **does not exist on this machine** |

Note: untracked local configs reference `/code-projects/operating-system/...` and `/code-projects/_global-configs/...` — those are VM paths, not available locally.

## Pages

| Path | Purpose |
|---|---|
| `index.html` | Main player — fetches `_data/songs.json`, audio player |
| `upload/index.html` | Staticrypt-encrypted upload form (password-protected via AES-CBC) |
| `manage/index.html` | Delete songs — requires `sessionStorage.whisper_token`, talks to GitHub Contents API |

## Design token workflow

Single source of truth: `tooling/_design/tokens.json` (flat key format, e.g. `font.size_body`).

1. Edit `tooling/_design/tokens.json`
2. Run `python3 tooling/_design/apply_tokens.py` — replaces only the `/* WHISPERING-GENERATED */` `<style>` blocks in `index.html` and `manage/index.html`; `WHISPERING-PAGE-SPECIFIC` override blocks survive (upload page is encrypted; its styling is set at re-encrypt time via the template)
3. Run `python3 tooling/_design/validate_design.py` — exits 1 if any token missing from any plaintext page
4. Run `bash tooling/deploy_guardrails.sh` — pre-push checks (bold tokens, hardcoded PAT, design consistency, token validity via GitHub API)
5. If upload changed: re-encrypt with Staticrypt, then `bash tooling/audit_staticrypt.sh`
6. Push

Note: there is no `_design/` W3C pipeline and no `styles.css` anymore — removed as dead code. The `generate_css.py` script produces the CSS block that `apply_tokens.py` injects.

## Style rules

- **Font-weight: 200 everywhere. No bold.**
- Accent: cyan `#00C3E1`; home-page logo only uses `#00DDFF` (slightly more saturated/lighter) via `index.html`'s page-specific block.
- **Fluid flex layout:** no fixed padding breakpoints. Side margins `clamp(16px, 5vw, 80px)`, top `clamp(24px, 4vw, 48px)`; `min-height: 100svh`; `min-width: 0` + `overflow-wrap: anywhere` on flex text children; nothing clips (see ARCHITECTURE.md → Layout System).
- Font family: `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`
- Body font size: `font.size_body` in tokens.json (e.g. "10pt"). No `font_scale` key.
- To resize text: edit `font.size_body` in tokens, then run apply_tokens.

## Staticrypt (upload page)

Template: `template.html` with placeholders (`/*[|template_title|]*/`, `/*[|js_staticrypt|]*/`, `/*[|encrypted_content|]*/`).
Audit with: `bash tooling/audit_staticrypt.sh FILE TITLE PLACEHOLDER PASSWORD`
- Password must NOT appear in plaintext in output
- Placeholder must be generic (e.g. "password"), never the real password
- `<title>`, cyan color, and Inter font are verified

## Security

- **Never commit `github_pat_*` tokens in plaintext.** Auto-revoked by GitHub when found in public repos.
- The current PAT lives **only** inside the staticrypt-encrypted blob of `upload/index.html` (decryptable, but not plaintext). Do NOT copy it into plaintext source files.
- Supply a PAT at push/CI time via `$GH_TOKEN` env var or `~/.gh_token` file.
- The PAT is also used at runtime by the upload page (stored in `sessionStorage.whisper_token`) — this leaks to public JS. Known issue.

## Known bugs

- Manage page displays "can't load content" error

## Playwright tests

Config at `playwright.config.ts` — uses **Brave Browser** (not Chrome). Run with `npx playwright test`. No tests exist yet.

## macOS gotchas

- `grep -P` is not available. Use `grep -oE 'github_pat_[A-Za-z0-9_]*'` instead.
- No `/root/` dir. Token file is `~/.gh_token`.

## CI/CD + hooks

- **CI workflow is NOT pushed yet.** `.github/workflows/guardrails.yml` was written but excluded from the last push because the PAT lacks `workflow` scope (GitHub refuses PAT pushes that create/update workflow files without it). Re-add it once a workflow-scoped PAT exists: re-create `.github/workflows/guardrails.yml` (checks `bash tooling/deploy_guardrails.sh`, `GH_TOKEN: ${{ secrets.GH_TOKEN || github.token }}`).
- Local pre-push hook: `tooling/hooks/pre-push` — runs guardrails before every push. Install once with `git config core.hooksPath tooling/hooks` (already configured).
- Everything is manual-only until CI lands: `bash tooling/deploy_guardrails.sh` before pushing.
- `git/hooks/pre-push.sh` is a VM artifact — ignore it on this machine (points at non-existent `/code-projects/operating-system/guardrails.sh`).
