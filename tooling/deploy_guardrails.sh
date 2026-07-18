#!/bin/bash
# deploy_guardrails.sh — Run BEFORE every push to the whispering site.
# Checks real repo invariants for github.com/pointy-secrets/whispering (branch: main).
# Fails closed (exit 1) on any violation.
set -u
cd "$(dirname "$0")/.."   # repo root (tooling/ lives under repo root)
FAIL=0
WARN=0
pass(){ echo "  [OK] $1"; }
fail(){ echo "  [FAIL] $1"; FAIL=1; }
warn(){ echo "  [WARN] $1"; WARN=1; }

echo "=============================================="
echo "  WHISPERING SITE - DEPLOY GUARDRAILS"
echo "=============================================="

# ---------- 1. MAIN PAGE (index.html) ----------
echo "[1] Main page (index.html)"
if [ ! -f index.html ]; then fail "index.html missing"; else
  B=$(grep -oE "font-weight: [4-9][0-9]?[0-9]?" index.html | wc -l)
  BW=$(grep -iwc "bold" index.html)
  if [ "$B" -gt 0 ] || [ "$BW" -gt 0 ]; then fail "bold/heavy font-weight present"; else pass "no bold weights"; fi
  grep -q "font-weight: 200" index.html && pass "light weight 200 present" || warn "no font-weight:200"
  grep -q "Doorway" index.html && pass "'Doorway' menu item present" || warn "Doorway missing"
  grep -q "Voices" index.html && pass "'Voices' filter present" || warn "Voices missing"
  grep -q "24px" index.html && pass "24px padding present" || warn "24px padding not found"
fi

# ---------- 2. MANAGE PAGE (manage/index.html) ----------
echo "[2] Manage page (manage/index.html)"
if [ ! -f manage/index.html ]; then fail "manage/index.html missing"; else
  B=$(grep -oE "font-weight: [4-9][0-9]?[0-9]?" manage/index.html | wc -l)
  BW=$(grep -iwc "bold" manage/index.html)
  if [ "$B" -gt 0 ] || [ "$BW" -gt 0 ]; then fail "bold/heavy font-weight present"; else pass "no bold weights"; fi
  grep -q "font-weight: 200" manage/index.html && pass "light weight 200 present" || warn "no font-weight:200"
  grep -q "github_pat_" manage/index.html && fail "token hardcoded in manage (must not be)" || pass "no hardcoded token in manage"
fi

# ---------- 3. UPLOAD ENCRYPTED (upload/index.html) ----------
echo "[3] Upload encrypted (upload/index.html)"
if [ ! -f upload/index.html ]; then fail "upload/index.html missing"; else
  if bash tooling/audit_staticrypt.sh upload/index.html "whispering!" "password" "screaming" >/dev/null 2>&1; then
    pass "staticrypt audit passed"
  else
    fail "staticrypt audit failed"
  fi
fi

# ---------- 4. UPLOAD SOURCE (upload.html) ----------
echo "[4] Upload source (upload.html)"
if [ ! -f upload.html ]; then warn "upload.html missing (only encrypted upload/index.html present)"; else
  grep -q "github_pat_" upload.html && fail "token hardcoded in upload source (must not be)" || pass "no hardcoded token in upload source"
  B=$(grep -oE "font-weight: [4-9][0-9]?[0-9]?" upload.html | wc -l)
  BW=$(grep -iwc "bold" upload.html)
  if [ "$B" -gt 0 ] || [ "$BW" -gt 0 ]; then fail "bold/heavy font-weight present"; else pass "no bold weights"; fi
fi

# ---------- 5. TOKEN VALIDITY (uses $GH_TOKEN or /root/.gh_token, never a hardcoded one) ----------
echo "[5] GitHub token validity"
if [ -n "${GH_TOKEN:-}" ]; then TOKEN="$GH_TOKEN"
elif [ -f /root/.gh_token ]; then TOKEN="$(cat /root/.gh_token)"
else TOKEN=""; fi
if [ -z "$TOKEN" ]; then warn "no GH_TOKEN available - skipping API check"; else
  CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 -H "Authorization: Bearer $TOKEN" "https://api.github.com/repos/pointy-secrets/whispering/contents/_data/songs.json")
  if [ "$CODE" = "200" ]; then pass "token valid (API 200)"; else fail "token invalid (API $CODE) - reissue needed"; fi
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "[RESULT] ALL GUARDRAILS PASSED - safe to push"
  exit 0
else
  echo "[RESULT] GUARDRAILS FAILED - DO NOT PUSH until fixed"
  exit 1
fi
