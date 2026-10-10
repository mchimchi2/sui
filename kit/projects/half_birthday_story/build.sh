#!/bin/bash
# 写真13枚+動画(input/half_birthday/)→ ストーリー用動画 out/half_birthday_story_ig.mp4
set -e
cd "$(dirname "$0")"
mkdir -p assets out
[ -f assets/gsap.min.js ] || { npm i gsap@3 --silent && cp node_modules/gsap/dist/gsap.min.js assets/; }
python3 prepare.py   # 写真を9:16に切り抜き+明るさ調整、動画をHDR→SDR
python3 music.py     # パリピ風オリジナルBGM(128BPM)
python3 build.py     # index.html
npx --yes hyperframes lint .
npx --yes hyperframes render -f 30 -q standard -o out/half_birthday_story.mp4 .
ffmpeg -v error -y -i out/half_birthday_story.mp4 -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart out/half_birthday_story_ig.mp4
echo "✓ out/half_birthday_story_ig.mp4"
