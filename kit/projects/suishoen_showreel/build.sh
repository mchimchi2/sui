#!/bin/bash
# 3つの10秒パートを生成→レンダー→連結→音楽を合成して out/suishoen_showreel_30s.mp4 を作る
set -e
cd "$(dirname "$0")"
[ -f assets/gsap.min.js ] || { npm i gsap@3 --silent && cp node_modules/gsap/dist/gsap.min.js assets/; }
[ -f assets/music.wav ] || ffmpeg -v error -y -i assets/music_raw.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 assets/music.wav
python3 gen.py      # p1 (と旧版p2,p3)
python3 gen2.py     # p2,p3 最新版(懐石・動画入り)で上書き
mkdir -p out
for p in p1 p2 p3; do
  mkdir -p $p; cp $p.html $p/index.html; ln -sfn ../assets $p/assets; cp template/hyperframes.json $p/
  (cd $p && npx --yes hyperframes lint)
  (cd $p && npx --yes hyperframes render -f 30 -q standard -o ../out/$p.mp4)
done
printf "file %s\n" p1.mp4 p2.mp4 p3.mp4 > out/list.txt
ffmpeg -v error -y -f concat -safe 0 -i out/list.txt -i assets/music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/suishoen_showreel_30s.mp4
echo "✓ out/suishoen_showreel_30s.mp4"
