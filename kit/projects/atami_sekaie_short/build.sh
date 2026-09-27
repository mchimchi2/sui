#!/bin/bash
# 台本(script.json) → 声 → 音 → 画面 → 検査 → 書き出し → out/atami_sekaie_short.mp4
set -e
cd "$(dirname "$0")"
mkdir -p assets out
[ -f assets/gsap.min.js ] || { npm i gsap@3 --silent && cp node_modules/gsap/dist/gsap.min.js assets/; }
python3 ../../assets/character/make_poses.py   # 表情差分(真顔/笑顔/びっくり × 口3段)
python3 voice.py                               # 台詞の声 + 口パク用の音量 → timing.json
python3 audio.py                               # BGM+効果音+声 を1本に → assets/mix.wav
python3 build.py                               # index.html
npx --yes hyperframes lint .
npx --yes hyperframes render -f 30 -q standard -o out/atami_sekaie_short.mp4 .
echo "✓ out/atami_sekaie_short.mp4"
