#!/bin/bash
# Self-audit for Staticrypt-encrypted upload page
# Usage: ./audit_staticrypt.sh <file> <expected_title> <expected_placeholder> <password_value>
FILE="$1"
TITLE="$2"
PLACEHOLDER="$3"
PASSWORD="$4"

echo "=== STATICRYPT AUDIT: $FILE ==="

# 1. Password must NOT appear in plaintext
PCOUNT=$(grep -o "$PASSWORD" "$FILE" | wc -l)
if [ "$PCOUNT" -gt 0 ]; then
  echo "❌ FAIL: password appears $PCOUNT times in plaintext"
  exit 1
else
  echo "✅ PASS: password not in plaintext"
fi

# 2. Placeholder must be generic (not the password)
PH=$(grep -o "placeholder=\"[^\"]*\"" "$FILE" | head -1)
if echo "$PH" | grep -q "$PASSWORD"; then
  echo "❌ FAIL: placeholder contains password: $PH"
  exit 1
else
  echo "✅ PASS: placeholder is generic: $PH"
fi

# 3. Title check
if grep -q "<title>$TITLE</title>" "$FILE"; then
  echo "✅ PASS: title is '$TITLE'"
else
  echo "❌ FAIL: title mismatch"
  exit 1
fi

# 4. Custom CSS present
if grep -q "00C3E1" "$FILE"; then
  echo "✅ PASS: custom cyan styling present"
else
  echo "❌ FAIL: custom styling missing"
  exit 1
fi

# 5. Inter font present
if grep -q "Inter" "$FILE"; then
  echo "✅ PASS: Inter font present"
else
  echo "❌ FAIL: Inter font missing"
  exit 1
fi

echo "=== ALL CHECKS PASSED ==="
exit 0
