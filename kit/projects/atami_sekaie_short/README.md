# ちび審査員が行く #01 ATAMI せかいえ(ショート・約36秒)

ちび審査員が口パクで喋って解説する版。未宿泊回なので、宿の映像は使わず事実情報のカード+自作グラフィックのみ。

## 作り直し
```
pip install pyopenjtalk-plus scipy pillow numpy   # 声(OpenJTalk)・画像処理
bash build.sh
```
台詞を変えるときは `script.json` を編集 → `bash build.sh`。
- `voice` = 読み上げ用の文(読み間違い対策でかな書き可)、`telop` = 画面の文字(正しい表記)
- `pose` = serious / smile / shock、`shot` = wide / close(寄り)、`card` = 上半分に出す情報カード

## 仕組み
| ファイル | 役割 |
|---|---|
| ../../assets/character/make_poses.py | オーナー作成のちび審査員画像から、背景透過+表情3種×口3段を作る |
| voice.py | OpenJTalk で読み上げ→ rubberband で声を高く。1/30秒ごとの音量から口の開きを計算 |
| audio.py | 128BPMのオリジナルBGM(numpy)+効果音+声を1本に。声の間はBGMを28%に下げる。-14 LUFS 目標 |
| build.py / style.css | HyperFrames の index.html を生成(袋文字テロップ・回る集中線・紙吹雪・寄り引きカット) |

## 本番に向けた差し替え候補
- 声: OpenJTalk は機械っぽい。ElevenLabs 等に替えるなら voice.py だけ差し替え(timing.json の形式を守る)
- 動き: AI動画(Kling 等)で作ったクリップに差し替えるなら、キャラ部分を <video> にするだけで他はそのまま

## 確認済み(2026-09-28)
- lint エラー0。書き出し 1080×1920・30fps・35.6秒
- whisper で声を書き起こして台本と照合(「せかいえ棟」の読み違いを修正済み。会席/解析など同音語はテロップで補う)
- ラウドネスは -15.1 LUFS(1パスの loudnorm。-14 ぴったりにするなら2パスに)
