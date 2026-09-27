# 子連れ旅行インスタ「ちび審査員」制作キット

このフォルダは claude.ai のチャットから引き継いだプロジェクトです。作業を始める前に `docs/` の3ファイルを必ず読んでください。

- `docs/strategy.md` … アカウントの方針・目標・役割分担・投稿ルール(最重要)
- `docs/hotels.md` … 旅行に行かずに作る最初の9本の宿候補と出典
- `docs/lessons.md` … 動画制作で踏んだ罠と対処(作業前に必読)

## 役割
- 私(Claude)= 企画・動画制作・マーケティング・営業資料
- オーナー = 撮影、投稿、ストーリー

## フォルダ構成
```
input/                        手元の写真・動画を元のファイル名のまま置く(IMG_xxxx.jpeg / .mov)
projects/hakone_first_trip/   家族旅行シネマティック動画(Python版とHyperFrames版)
projects/suishoen_showreel/   翠松園30秒ショーリール(HyperFrames、3パート×10秒)
projects/atami_sekaie_reel/   ATAMI せかいえ「行きたい宿リスト」リール(未宿泊・自作グラフィック)
docs/                         方針・宿リスト・教訓
```

## 必要な道具
Node.js、Python3 (Pillow, numpy, scipy, opencv-python)、FFmpeg(zscale付き)、日本語明朝フォント(Noto Serif CJK JP 推奨)。
不足は `npx hyperframes doctor` で確認。

## 再現手順
### 翠松園ショーリール
```
cd projects/suishoen_showreel
python3 prepare_assets.py      # input/ から素材作成(人物トリミング・献立の氏名消し・HDR変換)
python3 music.py               # オリジナルBGM(120BPM)を作曲
bash build.sh                  # 3パートをレンダー→連結→BGM合成 → out/suishoen_showreel_30s.mp4
```
### 箱根家族旅行動画
```
cd projects/hakone_first_trip
python3 stills.py              # 絵コンテ静止画(sheet.png)
python3 render.py              # Python版の本編(無音) → out_noaudio.mp4
# HyperFrames版: python3 prepare_hf_assets.py → hyperframes_index.html を index.html にして render
```

## 作業ルール
- 新しい動画は、まず「絵コンテ静止画」を見せてOKをもらってから書き出す
- 書き出し後は必ず数フレームを画像で確認(人物の写り込み・文字崩れ・名前の写り込み)
- 学んだことは `docs/lessons.md` に追記する
