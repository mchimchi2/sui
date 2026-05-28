#!/bin/bash
set -e

OUT="out"
mkdir -p "$OUT"

TOTAL=30
SUCCESS=0
FAIL=0

echo "=== 全${TOTAL}本レンダリング開始 ==="

for i in $(seq 1 $TOTAL); do
  ID=$(printf "kyujinhyo-%02d" $i)
  FILE="${OUT}/${ID}.mp4"

  if [ -f "$FILE" ]; then
    echo "[SKIP] $ID (already exists)"
    SUCCESS=$((SUCCESS + 1))
    continue
  fi

  echo "[RENDER] $ID ..."
  if npx remotion render "$ID" "$FILE" --log=error 2>&1; then
    echo "[OK] $ID"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "[FAIL] $ID"
    FAIL=$((FAIL + 1))
  fi
done

echo ""
echo "=== 完了: ${SUCCESS}本成功 / ${FAIL}本失敗 ==="
ls -lh "$OUT"/*.mp4 2>/dev/null | awk '{print $5, $9}'
